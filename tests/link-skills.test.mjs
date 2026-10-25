import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, lstatSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const script = join(repo, 'scripts/link-skills.sh');
const skillCount = readdirSync(join(repo, 'skills'), { withFileTypes: true })
  .filter((g) => g.isDirectory())
  .flatMap((g) => readdirSync(join(repo, 'skills', g.name), { withFileTypes: true })
    .filter((s) => s.isDirectory() && existsSync(join(repo, 'skills', g.name, s.name, 'SKILL.md'))))
  .length;
const alwaysOn = readdirSync(join(repo, 'rules/core'))
  .filter((f) => /^alwaysApply:\s*true\s*$/m.test(readFileSync(join(repo, 'rules/core', f), 'utf8'))).length;
const agentCount = readdirSync(join(repo, 'agents')).filter((f) => f.endsWith('.md')).length;

function run(args) {
  const home = mkdtempSync(join(tmpdir(), 'levistack-link-'));
  execFileSync('bash', [script, ...args], { env: { ...process.env, HOME: home }, stdio: 'pipe' });
  return home;
}

test('--trae links flat skills, prefixed agents and the always-on core rules', () => {
  const home = run(['--trae']);
  try {
    assert.equal(readdirSync(join(home, '.trae/skills')).length, skillCount);
    const agents = readdirSync(join(home, '.trae/agents'));
    assert.equal(agents.length, agentCount);
    assert.ok(agents.every((a) => a.startsWith('levistack-')));
    assert.equal(readdirSync(join(home, '.trae/rules')).length, alwaysOn);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('--antigravity builds a plugin folder with plugin.json and one-level skills', () => {
  const home = run(['--antigravity']);
  try {
    const plugin = join(home, '.gemini/config/plugins/levistack');
    assert.ok(lstatSync(join(plugin, 'plugin.json')).isSymbolicLink());
    const skills = readdirSync(join(plugin, 'skills'));
    assert.equal(skills.length, skillCount);
    assert.ok(skills.every((s) => existsSync(join(plugin, 'skills', s, 'SKILL.md'))));
    assert.equal(readdirSync(join(plugin, 'rules')).length, alwaysOn);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('never replaces a real folder that is not a symlink', () => {
  const home = mkdtempSync(join(tmpdir(), 'levistack-link-'));
  try {
    mkdirSync(join(home, '.trae/skills/tdd'), { recursive: true });
    writeFileSync(join(home, '.trae/skills/tdd/SKILL.md'), 'mine');
    const out = execFileSync('bash', [script, '--trae'], { env: { ...process.env, HOME: home } }).toString();
    assert.match(out, /skip \(exists, not a symlink\)/);
    assert.equal(readFileSync(join(home, '.trae/skills/tdd/SKILL.md'), 'utf8'), 'mine');
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('--cursor links flat skills and prefixed agents into ~/.cursor', () => {
  const home = run(['--cursor']);
  try {
    assert.equal(readdirSync(join(home, '.cursor/skills')).length, skillCount);
    const agents = readdirSync(join(home, '.cursor/agents'));
    assert.equal(agents.length, agentCount);
    assert.ok(agents.every((a) => a.startsWith('levistack-')));
    assert.equal(existsSync(join(home, '.cursor/rules')), false);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('--dry-run changes nothing', () => {
  const home = run(['--all', '--dry-run']);
  try {
    assert.deepEqual(readdirSync(home), []);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});
