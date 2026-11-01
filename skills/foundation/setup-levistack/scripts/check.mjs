#!/usr/bin/env node
// Check the runtimes and optional CLIs levistack scripts call, and render a status note.
// Usage: node check.mjs [--write] [--out <path>] [--json]
// Without --write it prints the note and writes nothing. It never installs anything.
import { spawnSync } from 'node:child_process';
import { accessSync, constants, mkdirSync, writeFileSync } from 'node:fs';
import { homedir, platform } from 'node:os';
import { delimiter, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const MIN_NODE = 20;

export const TOOLS = [
  { name: 'node', required: true, versionArgs: ['--version'], usedBy: 'Every Node script and npm run check', install: { darwin: 'brew install node', linux: 'Install Node 20+ from nodejs.org or your package manager' } },
  { name: 'python3', required: true, versionArgs: ['--version'], usedBy: 'Diagram, infographic, file-toolkit, convert-as-skill, and mcp-management scripts', install: { darwin: 'brew install python', linux: 'sudo apt install python3' } },
  { name: 'rsvg-convert', versionArgs: ['--version'], usedBy: 'diagram export_svg.py and infographic png_from_svg.py (SVG to PNG)', install: { darwin: 'brew install librsvg', linux: 'sudo apt install librsvg2-bin' } },
  { name: 'ffmpeg', versionArgs: ['-version'], usedBy: 'diagram animated export and Mermaid GIF encoding', install: { darwin: 'brew install ffmpeg', linux: 'sudo apt install ffmpeg' } },
  { name: 'mmdc', versionArgs: ['--version'], usedBy: 'diagram Mermaid to SVG or PNG', install: { darwin: 'npm install -g @mermaid-js/mermaid-cli', linux: 'npm install -g @mermaid-js/mermaid-cli' } },
  { name: 'playwright', python: 'playwright', usedBy: 'diagram mermaid_playwright_gif.py (Python package)', install: { darwin: 'pip install playwright && playwright install chromium', linux: 'pip install playwright && playwright install chromium' } },
  { name: 'glab', versionArgs: ['--version'], usedBy: 'code-review mr-context.sh (GitLab MR context)', install: { darwin: 'brew install glab', linux: 'See https://gitlab.com/gitlab-org/cli#installation' } },
  { name: 'jq', versionArgs: ['--version'], usedBy: 'code-review mr-context.sh', install: { darwin: 'brew install jq', linux: 'sudo apt install jq' } },
  { name: 'sqlite3', versionArgs: ['--version'], usedBy: 'standup collect.mjs browser history', install: { darwin: 'Preinstalled on macOS', linux: 'sudo apt install sqlite3' } },
  { name: 'pdftotext', versionArgs: ['-v'], usedBy: 'convert-as-skill extract_document.py (PDF text)', install: { darwin: 'brew install poppler', linux: 'sudo apt install poppler-utils' } },
];

export function which(name, env = process.env) {
  for (const dir of (env.PATH ?? '').split(delimiter)) {
    if (!dir) continue;
    const candidate = join(dir, name);
    try {
      accessSync(candidate, constants.X_OK);
      return candidate;
    } catch {}
  }
  return null;
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', timeout: 10000, stdio: ['ignore', 'pipe', 'pipe'] });
  return { status: r.status, out: `${r.stdout ?? ''}${r.stderr ?? ''}`.trim(), error: r.error };
}

function firstLine(text) {
  return (text.split('\n').find((line) => line.trim()) ?? '').trim().slice(0, 80);
}

export function probe(tool, { find = which, exec = run, nodeVersion = process.versions.node } = {}) {
  if (tool.python) {
    if (!find('python3')) return { ...tool, found: false, detail: 'python3 missing' };
    const r = exec('python3', ['-c', `import ${tool.python}; print(getattr(${tool.python}, '__version__', 'installed'))`]);
    return { ...tool, found: r.status === 0, detail: r.status === 0 ? firstLine(r.out) : 'module not importable' };
  }
  const path = find(tool.name);
  if (!path) return { ...tool, found: false, detail: 'not on PATH' };
  const r = exec(path, tool.versionArgs ?? ['--version']);
  const detail = firstLine(r.out) || path;
  if (tool.name === 'node') {
    const major = Number(nodeVersion.split('.')[0]);
    if (major < MIN_NODE) return { ...tool, found: false, detail: `node ${nodeVersion}, needs ${MIN_NODE}+` };
  }
  return { ...tool, found: true, detail };
}

export function check(options = {}) {
  return TOOLS.map((tool) => probe(tool, options));
}

export function render(results, { date = new Date().toISOString().slice(0, 10), os = platform() } = {}) {
  const key = os === 'darwin' ? 'darwin' : 'linux';
  const missingRequired = results.filter((r) => r.required && !r.found);
  const gaps = results.filter((r) => !r.required && !r.found);
  const row = (r) => `| \`${r.name}\` | ${r.found ? 'found' : 'missing'} | ${r.detail} | ${r.usedBy} |`;
  const lines = [
    '# levistack setup',
    '',
    `Checked ${date} on ${os}. Rerun \`/setup-levistack\` to refresh; it overwrites this note.`,
    '',
    `Status: ${missingRequired.length ? `blocked, ${missingRequired.map((r) => r.name).join(', ')} missing` : gaps.length ? `ready with ${gaps.length} named gap(s)` : 'ready'}`,
    '',
    '| Tool | State | Detail | Used by |',
    '|---|---|---|---|',
    ...results.map(row),
  ];
  const todo = [...missingRequired, ...gaps];
  if (todo.length) {
    lines.push('', '## Gaps', '', 'Each missing tool stops only the step that needs it. Nothing was installed.', '');
    for (const r of todo) lines.push(`- \`${r.name}\`${r.required ? ' (required)' : ''}: ${r.install[key]}`);
  }
  return `${lines.join('\n')}\n`;
}

export function defaultNotePath(home = homedir()) {
  return join(home, '.levistack', 'setup.md');
}

function main(argv) {
  const write = argv.includes('--write');
  const outIndex = argv.indexOf('--out');
  const out = outIndex >= 0 ? argv[outIndex + 1] : defaultNotePath();
  if (outIndex >= 0 && !out) {
    console.error('--out needs a path');
    return 2;
  }
  const results = check();
  if (argv.includes('--json')) {
    console.log(JSON.stringify(results.map(({ name, required, found, detail }) => ({ name, required: Boolean(required), found, detail })), null, 2));
  } else {
    process.stdout.write(render(results));
  }
  if (write) {
    mkdirSync(dirname(out), { recursive: true });
    writeFileSync(out, render(results));
    console.error(`wrote ${out}`);
  }
  return results.some((r) => r.required && !r.found) ? 1 : 0;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) process.exitCode = main(process.argv.slice(2));
