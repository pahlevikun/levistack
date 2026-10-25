import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { render, detectRuntime } from '../statusline/statusline.mjs';
import { CODEX_ITEMS, install, removeTomlStatusLine, setTomlStatusLine } from '../scripts/install-statusline.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const script = join(repo, 'statusline', 'statusline.mjs');
const deps = { email: () => 'dev@example.com', branch: () => 'main' };
const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');

const claude = {
  model: { display_name: 'Sonnet 5.5' },
  workspace: { current_dir: '/work/levistack' },
  context_window: { used_percentage: 30 },
  rate_limits: { five_hour: { used_percentage: 60 }, seven_day: { used_percentage: 20 } },
  effort: { level: 'medium' },
  thinking: { enabled: true },
};

const cursor = {
  session_id: 's1',
  render_width_chars: 120,
  autorun: false,
  cwd: '/work/levistack',
  model: { id: 'claude-4-opus', display_name: 'Claude 4 Opus', param_summary: '(Thinking) High', max_mode: true },
  workspace: { current_dir: '/work/levistack' },
  context_window: { used_percentage: 34.5, remaining_percentage: 65.5 },
};

test('runtime detection tells the Cursor payload from the Claude payload', () => {
  assert.equal(detectRuntime(cursor), 'cursor');
  assert.equal(detectRuntime(claude), 'claude');
});

test('claude: one line in the agreed order with model, effort, thinking and gauges', () => {
  const line = strip(render(claude, { deps, color: false }));
  assert.equal(line, 'dev@example.com | levistack | main | Sonnet 5.5 Medium Thinking | 5h ▰▰▰▰▰▱▱▱ 60% | 1w ▰▰▱▱▱▱▱▱ 20% | ctx ▰▰▱▱▱▱▱▱ 30%');
  assert.ok(!line.includes('\n'));
});

test('cursor: hides what the payload lacks and reads effort and thinking from param_summary', () => {
  const line = strip(render(cursor, { deps: { email: () => null, branch: () => 'main' }, color: false }));
  assert.equal(line, 'levistack | main | Claude 4 Opus Max High Thinking | ctx ▰▰▰▱▱▱▱▱ 35%');
  assert.ok(!line.includes('5h') && !line.includes('1w'));
});

test('gauge colors: green below 60, yellow from 60, red from 85', () => {
  const at = (pct) => render({ ...claude, context_window: { used_percentage: pct } }, { deps, color: true, segments: ['ctx'] });
  assert.match(at(10), /\x1b\[32m/);
  assert.match(at(60), /\x1b\[33m/);
  assert.match(at(90), /\x1b\[31m/);
});

test('NO_COLOR style output has no escape codes', () => {
  assert.ok(!render(claude, { deps, color: false }).includes('\x1b'));
});

test('segments option chooses and orders segments', () => {
  const line = strip(render(claude, { deps, color: false, segments: ['model', 'dir'] }));
  assert.equal(line, 'Sonnet 5.5 Medium Thinking | levistack');
});

test('narrow terminals drop low-priority segments first and keep model and context', () => {
  const line = strip(render(claude, { deps, color: false, width: 60 }));
  assert.ok(line.length <= 60, line);
  assert.ok(line.includes('Sonnet 5.5'));
  assert.ok(line.includes('ctx'));
  assert.ok(!line.includes('dev@example.com'));
});

test('cli: garbage or empty stdin prints nothing and exits 0', () => {
  for (const input of ['not json', '', '[]', 'null']) {
    const r = spawnSync('node', [script, '--runtime=claude'], { input, encoding: 'utf8' });
    assert.equal(r.status, 0, input);
    assert.ok(!r.stdout.includes('undefined'));
  }
});

test('cli: renders a cursor payload end to end', () => {
  const r = spawnSync('node', [script, '--runtime=cursor'], {
    input: JSON.stringify(cursor),
    encoding: 'utf8',
    env: { ...process.env, NO_COLOR: '1' },
  });
  assert.equal(r.status, 0);
  assert.match(r.stdout, /Claude 4 Opus Max High Thinking/);
});

// ---- TOML editing ----------------------------------------------------------------------------

test('toml: appends [tui] and keeps unrelated tables untouched', () => {
  const src = '[mcp_servers.x]\ncommand = "x"\n';
  const r = setTomlStatusLine(src, ['git-branch']);
  assert.ok(r.text.startsWith(src));
  assert.match(r.text, /\[tui\]\n# managed by levistack: statusline\nstatus_line = \["git-branch"\]/);
});

test('toml: adds the key inside an existing [tui] table without touching its other keys', () => {
  const r = setTomlStatusLine('[tui]\ntheme = "dark"\n\n[other]\na = 1\n', ['model']);
  assert.match(r.text, /\[tui\]\n# managed by levistack: statusline\nstatus_line = \["model"\]\ntheme = "dark"/);
  assert.match(r.text, /\[other\]\na = 1/);
});

test('toml: refuses to replace a status_line it does not own unless forced, including multi-line arrays', () => {
  const src = '[tui]\nstatus_line = [\n  "model",\n  "git-branch",\n]\nnotifications = true\n';
  assert.ok(setTomlStatusLine(src, ['model']).skipped);
  const forced = setTomlStatusLine(src, ['current-dir'], { force: true });
  assert.match(forced.text, /status_line = \["current-dir"\]\nnotifications = true/);
  assert.ok(!forced.text.includes('"git-branch"'));
});

test('toml: install then remove restores the original and is idempotent', () => {
  const src = '[mcp_servers.x]\ncommand = "x"\n';
  const once = setTomlStatusLine(src, CODEX_ITEMS);
  const twice = setTomlStatusLine(once.text, CODEX_ITEMS);
  assert.equal(twice.changed, false);
  const removed = removeTomlStatusLine(once.text);
  assert.ok(removed.text.includes('[mcp_servers.x]'));
  assert.ok(!removed.text.includes('status_line'));
});

test('toml: dotted tui keys are reported, not edited', () => {
  assert.ok(setTomlStatusLine('tui.status_line = ["model"]\n', ['model']).error);
});

// ---- installer -------------------------------------------------------------------------------

function sandbox() {
  const root = mkdtempSync(join(tmpdir(), 'levistack-sl-'));
  const env = {
    LEVISTACK_HOME: join(root, 'lh'),
    CLAUDE_CONFIG_DIR: join(root, 'claude'),
    CURSOR_CONFIG_DIR: join(root, 'cursor'),
    CODEX_HOME: join(root, 'codex'),
  };
  for (const d of [env.CLAUDE_CONFIG_DIR, env.CURSOR_CONFIG_DIR, env.CODEX_HOME]) mkdirSync(d, { recursive: true });
  return { root, env };
}

test('installer: installs for all three tools, copies the script, and merges instead of replacing', () => {
  const { root, env } = sandbox();
  try {
    writeFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), JSON.stringify({ model: 'x', permissions: { allow: ['Read'] } }));
    writeFileSync(join(env.CURSOR_CONFIG_DIR, 'cli-config.json'), JSON.stringify({ editor: { vimMode: true } }));
    writeFileSync(join(env.CODEX_HOME, 'config.toml'), '[mcp_servers.x]\ncommand = "x"\n');

    const results = install({ env });
    assert.deepEqual(results.map((r) => r.status), ['installed', 'installed', 'installed']);
    assert.ok(existsSync(join(env.LEVISTACK_HOME, 'statusline.mjs')));

    const claudeCfg = JSON.parse(readFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), 'utf8'));
    assert.equal(claudeCfg.model, 'x');
    assert.deepEqual(claudeCfg.permissions, { allow: ['Read'] });
    assert.match(claudeCfg.statusLine.command, /statusline\.mjs --runtime=claude$/);
    const cursorCfg = JSON.parse(readFileSync(join(env.CURSOR_CONFIG_DIR, 'cli-config.json'), 'utf8'));
    assert.deepEqual(cursorCfg.editor, { vimMode: true });
    assert.match(cursorCfg.statusLine.command, /--runtime=cursor$/);
    assert.match(readFileSync(join(env.CODEX_HOME, 'config.toml'), 'utf8'), /status_line = \["current-dir", "git-branch"/);
    assert.ok(readdirSync(env.CLAUDE_CONFIG_DIR).some((f) => f.endsWith('.bak')), 'a backup was written');

    assert.deepEqual(install({ env }).map((r) => r.status), ['unchanged', 'unchanged', 'unchanged']);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('installer: leaves a foreign statusLine alone unless --force, and --dry-run writes nothing', () => {
  const { root, env } = sandbox();
  try {
    const mine = { type: 'command', command: 'echo custom' };
    writeFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), JSON.stringify({ statusLine: mine }));

    const dry = install({ env, runtimes: ['claude'], dryRun: true });
    assert.equal(dry[0].status, 'skipped');
    assert.equal(install({ env, runtimes: ['claude'] })[0].status, 'skipped');
    assert.deepEqual(JSON.parse(readFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), 'utf8')).statusLine, mine);

    assert.equal(install({ env, runtimes: ['claude'], force: true })[0].status, 'installed');
    const after = JSON.parse(readFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), 'utf8'));
    assert.match(after.statusLine.command, /statusline\.mjs/);
    const bak = readdirSync(env.CLAUDE_CONFIG_DIR).find((f) => f.endsWith('.bak'));
    assert.deepEqual(JSON.parse(readFileSync(join(env.CLAUDE_CONFIG_DIR, bak), 'utf8')).statusLine, mine, 'previous value recoverable');
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('installer: --uninstall removes only what levistack wrote', () => {
  const { root, env } = sandbox();
  try {
    writeFileSync(join(env.CODEX_HOME, 'config.toml'), '[mcp_servers.x]\ncommand = "x"\n');
    install({ env });
    const out = install({ env, uninstall: true });
    assert.ok(out.every((r) => r.status === 'removed'));
    assert.ok(!('statusLine' in JSON.parse(readFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), 'utf8'))));
    assert.ok(!readFileSync(join(env.CODEX_HOME, 'config.toml'), 'utf8').includes('status_line'));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('installer: invalid JSON config is reported and not modified', () => {
  const { root, env } = sandbox();
  try {
    writeFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), '{ not json');
    const r = install({ env, runtimes: ['claude'] });
    assert.equal(r[0].status, 'error');
    assert.equal(readFileSync(join(env.CLAUDE_CONFIG_DIR, 'settings.json'), 'utf8'), '{ not json');
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
