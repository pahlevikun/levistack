// Hook discovery: every `hooks/<name>.mjs` is a hook. It exports `meta` and a default handler.
import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;

// Order events appear in the generated hooks.json; unknown events sort after these.
export const EVENT_ORDER = ['SessionStart', 'UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'Notification', 'Stop', 'SubagentStop', 'PreCompact', 'SessionEnd'];

export function resolveHook(hooksDir, name) {
  if (typeof name !== 'string' || !NAME.test(name)) return null;
  const file = join(hooksDir, `${name}.mjs`);
  return existsSync(file) ? file : null;
}

export const listHookNames = (hooksDir) =>
  readdirSync(hooksDir)
    .filter((f) => f.endsWith('.mjs'))
    .map((f) => f.slice(0, -4))
    .sort();

export function lintMeta(name, meta, handler) {
  const problems = [];
  if (!NAME.test(name)) problems.push('file name must be kebab-case');
  if (typeof handler !== 'function') problems.push('needs a default export (the handler)');
  if (!meta || typeof meta !== 'object') return [...problems, 'needs `export const meta`'];
  if (typeof meta.event !== 'string' || !meta.event) problems.push('meta.event is required (a Claude Code hook event)');
  if (typeof meta.description !== 'string' || !meta.description || /\n/.test(meta.description)) problems.push('meta.description must be one line');
  if (meta.matcher !== undefined && typeof meta.matcher !== 'string') problems.push('meta.matcher must be a string');
  if (meta.optIn !== undefined && typeof meta.optIn !== 'boolean') problems.push('meta.optIn must be a boolean');
  if (meta.timeout !== undefined && !(Number.isInteger(meta.timeout) && meta.timeout > 0)) problems.push('meta.timeout must be a positive integer (seconds)');
  return problems;
}

// [{ name, file, meta, problems }] sorted by name. Never throws on a broken hook; it reports problems instead.
export async function loadHooks(hooksDir) {
  const hooks = [];
  for (const name of listHookNames(hooksDir)) {
    const file = join(hooksDir, `${name}.mjs`);
    try {
      const mod = await import(pathToFileURL(file).href);
      hooks.push({ name, file, meta: mod.meta ?? {}, problems: lintMeta(name, mod.meta, mod.default) });
    } catch (e) {
      hooks.push({ name, file, meta: {}, problems: [`failed to import (${e.message})`] });
    }
  }
  return hooks;
}
