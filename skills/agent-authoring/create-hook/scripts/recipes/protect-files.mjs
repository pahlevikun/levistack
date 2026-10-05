#!/usr/bin/env node
// PreToolUse on Edit|Write: deny edits to files that are generated or hold secrets.
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const PROTECTED = [/(^|\/)package-lock\.json$/, /(^|\/)\.env(\.[\w-]+)?$/, /(^|\/)credentials\.json$/, /(^|\/)generated\//];

try {
  const file = JSON.parse(readFileSync(0, 'utf8')).tool_input?.file_path ?? '';
  if (PROTECTED.some((re) => re.test(file))) {
    console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: `${basename(file)} is protected. Change its source or ask the user.` } }));
  }
} catch {
  // unreadable input: allow
}
