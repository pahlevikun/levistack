#!/usr/bin/env node
// Run a hook command against a sample payload and say what the harness would do with the result.
//
//   node try-hook.mjs --event PreToolUse --tool Bash --command "rm -rf /" [--expect ask] -- <hook command...>
//   node try-hook.mjs --event PreToolUse --tool Write --file-path src/a.ts -- node hook.mjs
//   node try-hook.mjs --event UserPromptSubmit --prompt "hello" -- node hook.mjs
//   node try-hook.mjs --json '{"hook_event_name":"Stop"}' -- node hook.mjs
//
// Options: --cwd <dir> (default: current), --timeout <seconds> (default 10),
//          --expect allow|block|ask|defer|context|stop|error (exit 1 when the decision differs).
// The payload follows Claude Code's hook input. Use --json for any other event or for Cursor.
import { spawnSync } from 'node:child_process';

const CONTEXT_EVENTS = new Set(['UserPromptSubmit', 'SessionStart']);

export function buildPayload({ event, tool, command, filePath, prompt, cwd }) {
  const payload = { session_id: 'try-hook', cwd, hook_event_name: event, permission_mode: 'default' };
  if (tool) {
    payload.tool_name = tool;
    payload.tool_input = {};
    if (command != null) payload.tool_input.command = command;
    if (filePath != null) payload.tool_input.file_path = filePath;
  }
  if (prompt != null) payload.prompt = prompt;
  return payload;
}

// Turn exit code + streams into the decision a Claude Code harness would reach.
export function interpret({ status, stdout, stderr }, event) {
  const notes = [];
  const out = stdout.trim();
  let json = null;
  if (out.startsWith('{') && out.endsWith('}')) {
    try {
      json = JSON.parse(out);
    } catch (e) {
      notes.push(`stdout looks like JSON but does not parse (${e.message}); the harness reports an error and proceeds`);
    }
  } else if (out) {
    notes.push(CONTEXT_EVENTS.has(event) ? 'plain stdout is added to the model context for this event' : 'plain stdout goes to the debug log only');
  }

  if (status === 2) return { decision: 'block', reason: stderr.trim() || json?.reason || '(no reason given)', notes };
  if (status !== 0 && !json) return { decision: 'error', reason: `exit ${status}: non-blocking error, the action proceeds`, notes };

  if (json) {
    const h = json.hookSpecificOutput ?? {};
    if (h.permissionDecision === 'deny') return { decision: 'block', reason: h.permissionDecisionReason ?? '', notes };
    if (h.permissionDecision === 'ask') return { decision: 'ask', reason: h.permissionDecisionReason ?? '', notes };
    if (h.permissionDecision === 'defer') return { decision: 'defer', reason: h.permissionDecisionReason ?? '', notes };
    if (json.decision === 'block') return { decision: 'block', reason: json.reason ?? '', notes };
    if (json.continue === false) return { decision: 'stop', reason: json.stopReason ?? '', notes };
    if (h.additionalContext) return { decision: 'context', reason: h.additionalContext, notes };
    if (h.permissionDecision === 'allow') return { decision: 'allow', reason: h.permissionDecisionReason ?? '', notes };
    if (json.systemMessage) notes.push(`shows the user: ${json.systemMessage}`);
    const known = new Set(['continue', 'stopReason', 'systemMessage', 'suppressOutput', 'terminalSequence', 'hookSpecificOutput', 'decision', 'reason']);
    const unknown = Object.keys(json).filter((k) => !known.has(k));
    if (unknown.length) notes.push(`unrecognized top-level field(s): ${unknown.join(', ')}`);
  }
  if (out && !json && CONTEXT_EVENTS.has(event)) return { decision: 'context', reason: out, notes };
  return { decision: 'allow', reason: '', notes };
}

function parseArgs(argv) {
  const cut = argv.indexOf('--');
  const head = cut === -1 ? argv : argv.slice(0, cut);
  const hook = cut === -1 ? [] : argv.slice(cut + 1);
  const opts = {};
  for (let i = 0; i < head.length; i++) {
    const a = head[i];
    if (!a.startsWith('--')) throw new Error(`unexpected argument "${a}"`);
    const key = a.slice(2);
    const value = head[++i];
    if (value === undefined) throw new Error(`--${key} needs a value`);
    opts[key] = value;
  }
  return { opts, hook };
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`try-hook: ${e.message}`);
    process.exit(2);
  }
  const { opts, hook } = parsed;
  if (!hook.length) {
    console.error('usage: try-hook.mjs [--event E --tool T --command C | --json J] [--expect D] -- <hook command...>');
    process.exit(2);
  }
  const cwd = opts.cwd ?? process.cwd();
  let payload;
  if (opts.json) {
    try {
      payload = JSON.parse(opts.json);
    } catch (e) {
      console.error(`try-hook: --json is not valid JSON (${e.message})`);
      process.exit(2);
    }
  } else {
    if (!opts.event) {
      console.error('try-hook: pass --event (or --json)');
      process.exit(2);
    }
    payload = buildPayload({ event: opts.event, tool: opts.tool, command: opts.command, filePath: opts['file-path'], prompt: opts.prompt, cwd });
  }
  const event = payload.hook_event_name ?? payload.event ?? opts.event ?? '';
  const started = Date.now();
  const r = spawnSync(hook[0], hook.slice(1), {
    cwd,
    input: JSON.stringify(payload),
    encoding: 'utf8',
    timeout: (Number(opts.timeout) || 10) * 1000,
  });
  const ms = Date.now() - started;
  if (r.error) {
    const why = r.error.code === 'ETIMEDOUT' ? `timed out after ${opts.timeout ?? 10}s` : r.error.message;
    console.error(`try-hook: could not run the hook: ${why}`);
    process.exit(r.error.code === 'ETIMEDOUT' ? 1 : 2);
  }
  const result = interpret({ status: r.status, stdout: r.stdout ?? '', stderr: r.stderr ?? '' }, event);
  console.log(`event:    ${event}`);
  console.log(`exit:     ${r.status} (${ms} ms)`);
  console.log(`decision: ${result.decision}${result.reason ? ` - ${result.reason}` : ''}`);
  for (const n of result.notes) console.log(`note:     ${n}`);
  if (r.stdout?.trim()) console.log(`stdout:   ${r.stdout.trim()}`);
  if (r.stderr?.trim()) console.log(`stderr:   ${r.stderr.trim()}`);
  if (opts.expect && opts.expect !== result.decision) {
    console.error(`try-hook: expected "${opts.expect}" but got "${result.decision}"`);
    process.exit(1);
  }
}

import { fileURLToPath } from 'node:url';
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
