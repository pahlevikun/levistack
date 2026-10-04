#!/usr/bin/env node
// Audit AGENTS.md / CLAUDE.md instruction files under a directory.
//
//   node audit.mjs [dir] [--json] [--strict]
//
// Reports each instruction file with its size, then findings:
//   too-long        more lines than Claude's ~200-line guidance
//   empty           Codex skips empty files
//   claude-hides    CLAUDE.md beside AGENTS.md that does not import or link it, so Claude Code ignores AGENTS.md
//   local-hides     CLAUDE.local.md with no CLAUDE.md: it counts as a CLAUDE.md and hides AGENTS.md from Claude
//   chain-too-large root-to-leaf AGENTS.md bytes exceed Codex's 32 KiB default budget
//   override        AGENTS.override.md is read by Codex only
//   missing-path    a backticked path that does not exist
//   secret-like     text that looks like a credential
// Exit code is 0 unless --strict is given and a warning was found.
import { existsSync, lstatSync, readdirSync, readFileSync, realpathSync } from 'node:fs';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const NAMES = ['AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', 'CLAUDE.local.md'];
export const CODEX_LIMIT = 32 * 1024;
export const LINE_WARN = 200;
const SKIP = new Set(['node_modules', '.git', 'dist', 'build', 'target', 'vendor', '_build', 'deps', '.venv', '.next', 'coverage']);
const SECRET = /\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})\b|(?:api[_-]?key|secret|token|password)\s*[:=]\s*['"][A-Za-z0-9_\-]{16,}['"]/i;

export function findFiles(root) {
  const out = [];
  const walk = (dir) => {
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const p = join(dir, e.name);
      if (e.isDirectory()) {
        if (!SKIP.has(e.name)) walk(p);
      } else if (NAMES.includes(e.name)) {
        const st = lstatSync(p);
        const link = st.isSymbolicLink() ? realpathSync(p) : null;
        const text = readFileSync(p, 'utf8');
        out.push({
          path: p,
          dir,
          name: e.name,
          link,
          bytes: Buffer.byteLength(text),
          lines: text === '' ? 0 : text.replace(/\n$/, '').split('\n').length,
          text,
        });
      }
    }
  };
  walk(root);
  return out.sort((a, b) => a.path.localeCompare(b.path));
}

function pathTokens(text) {
  const withoutFences = text.replace(/```[\s\S]*?```/g, '');
  const tokens = new Set();
  for (const m of withoutFences.matchAll(/`([^`\n]+)`/g)) {
    const t = m[1].trim();
    if (/[\s*<>{}$|&;()=@]/.test(t) || /^(https?:|\/|~|#)/.test(t) || t.includes('...')) continue;
    if (/^[\w.-]+(\/[\w.-]+)+\/?$/.test(t) || /^\.?\/?[\w-]+\.(md|json|toml|ya?ml|mjs|cjs|js|ts|tsx|go|ex|exs|py|rs|sh)$/.test(t)) {
      tokens.add(t.replace(/^\.\//, ''));
    }
  }
  return [...tokens];
}

export function audit(rootArg) {
  const root = resolve(rootArg);
  const files = findFiles(root);
  const findings = [];
  const add = (severity, code, file, message) =>
    findings.push({ severity, code, file: relative(root, file.path) || file.name, message });

  const byDir = new Map();
  for (const f of files) {
    if (!byDir.has(f.dir)) byDir.set(f.dir, {});
    byDir.get(f.dir)[f.name] = f;
  }

  for (const f of files) {
    if (f.link) continue; // a symlink is the same text as its target, which is checked on its own
    if (f.bytes === 0 || f.text.trim() === '') add('warn', 'empty', f, 'file is empty; Codex skips empty files');
    if (f.lines > LINE_WARN) add('warn', 'too-long', f, `${f.lines} lines; keep under about ${LINE_WARN}`);
    if (SECRET.test(f.text)) add('warn', 'secret-like', f, 'looks like a credential; remove it');
    if (f.name === 'AGENTS.override.md') add('info', 'override', f, 'read by Codex only; Claude Code and Cursor ignore it');
    for (const token of pathTokens(f.text)) {
      if (!existsSync(join(f.dir, token)) && !existsSync(join(root, token))) {
        add('warn', 'missing-path', f, `path not found: ${token}`);
      }
    }
  }

  for (const [dir, set] of byDir) {
    const agents = set['AGENTS.md'];
    const claude = set['CLAUDE.md'];
    if (agents && claude) {
      const linked = claude.link && realpathSync(agents.path) === claude.link;
      const imports = /^\s*@(?:\.\/)?AGENTS\.md\b/m.test(claude.text);
      if (!linked && !imports) {
        add('warn', 'claude-hides', claude, 'Claude Code reads this instead of AGENTS.md here; add `@AGENTS.md` or symlink it');
      }
    }
    if (agents && !claude && set['CLAUDE.local.md']) {
      add('warn', 'local-hides', set['CLAUDE.local.md'], 'counts as a CLAUDE.md and stops Claude Code reading AGENTS.md; import it or use `@AGENTS.md`');
    }
  }

  const pick = (set) => set['AGENTS.override.md'] ?? set['AGENTS.md'];
  for (const [dir, set] of byDir) {
    if (!pick(set)) continue;
    let total = 0;
    for (const [d, s] of byDir) {
      const p = pick(s);
      if (p && (dir === d || dir.startsWith(d + sep))) total += p.bytes;
    }
    if (total > CODEX_LIMIT) {
      add('warn', 'chain-too-large', pick(set), `root-to-here AGENTS.md chain is ${total} bytes; Codex stops at ${CODEX_LIMIT}`);
    }
  }

  return { root, files: files.map(({ text, ...rest }) => ({ ...rest, path: relative(root, rest.path) || rest.name, dir: relative(root, rest.dir) || '.' })), findings };
}

function format(result) {
  const lines = [`Instruction files under ${result.root}`];
  if (!result.files.length) lines.push('  (none found)');
  for (const f of result.files) lines.push(`  ${f.path}  ${f.lines} lines, ${f.bytes} bytes${f.link ? ' (symlink)' : ''}`);
  lines.push('');
  if (!result.findings.length) lines.push('No findings.');
  for (const x of result.findings) lines.push(`${x.severity.toUpperCase().padEnd(5)} ${x.code.padEnd(15)} ${x.file}: ${x.message}`);
  return lines.join('\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const dir = args.find((a) => !a.startsWith('--')) ?? '.';
  const result = audit(dir);
  console.log(args.includes('--json') ? JSON.stringify(result, null, 2) : format(result));
  if (args.includes('--strict') && result.findings.some((f) => f.severity === 'warn')) process.exitCode = 1;
}
