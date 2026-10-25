// Inject a short digest of rules/core/*.md as context (Claude plugins cannot load rules natively).
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { allow, note } from './lib/result.mjs';

export const meta = {
  event: 'SessionStart',
  matcher: 'startup|resume|clear|compact',
  description: 'Injects a short digest of the always-on rules in `rules/core/` as context',
};

const MAX_CHARS = 4000;

export default function sessionStart({ root }) {
  const dir = join(root, 'rules', 'core');
  if (!existsSync(dir)) return allow();
  const parts = readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .sort()
    .map((f) => ({ f, text: readFileSync(join(dir, f), 'utf8') }))
    .filter(({ text }) => /^alwaysApply:\s*true\s*$/m.test(text))
    .map(({ f, text }) => {
      const body = text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '').trim();
      return `## ${f.replace(/\.md$/, '')}\n${body}`;
    });
  if (!parts.length) return allow();
  const digest = `Levistack rules:\n\n${parts.join('\n\n')}`;
  return note(digest.length > MAX_CHARS ? `${digest.slice(0, MAX_CHARS)}\n[truncated]` : digest);
}
