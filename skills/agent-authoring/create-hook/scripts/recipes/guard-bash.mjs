#!/usr/bin/env node
// PreToolUse on Bash: deny a few commands that are almost never intended, ask on force pushes.
// Fails open: any parse problem exits 0 with no output, so the command proceeds.
// A guard like this is a seat belt, not a sandbox: it cannot see every way to say the same thing.
import { readFileSync } from 'node:fs';

// `rm` with a recursive flag (any spelling, flags may be split) aimed at /, ~ or $HOME, with or without a trailing / or *.
function deletesHome(command) {
  for (const segment of command.split(/&&|\|\||;|\|/)) {
    const words = segment.trim().split(/\s+/);
    const at = words[0] === 'sudo' ? 1 : 0;
    if (words[at] !== 'rm') continue;
    const args = words.slice(at + 1);
    const recursive = args.some((a) => a === '--recursive' || /^-[a-zA-Z]*[rR]/.test(a));
    const aimedAtRoot = args.filter((a) => !a.startsWith('-')).some((a) => /^["']?(\/|~|\$HOME)\/?\*?["']?$/.test(a));
    if (recursive && aimedAtRoot) return true;
  }
  return false;
}

const DENY = [
  [deletesHome, 'recursive delete of /, ~ or $HOME'],
  [/\bmkfs(\.\w+)?\b/, 'formatting a filesystem'],
  [/>\s*\/dev\/(sd|nvme|disk)/, 'writing to a raw disk'],
];
const ASK = [
  [/\bgit\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b)/, 'force push'],
  [/\bgit\s+reset\s+--hard\b/, 'hard reset'],
];

const matches = (test, command) => (typeof test === 'function' ? test(command) : test.test(command));
const reply = (decision, reason) =>
  console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: decision, permissionDecisionReason: reason } }));

try {
  const command = JSON.parse(readFileSync(0, 'utf8')).tool_input?.command ?? '';
  for (const [test, why] of DENY) if (matches(test, command)) { reply('deny', `Blocked: ${why}.`); process.exit(0); }
  for (const [test, why] of ASK) if (matches(test, command)) { reply('ask', `Confirm: ${why}.`); process.exit(0); }
} catch {
  // unreadable input: allow
}
