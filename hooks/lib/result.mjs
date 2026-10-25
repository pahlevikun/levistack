// What a hook returns, independent of the agent runtime. `render` turns it into stdout/stderr/exit code.
export const allow = () => ({ kind: 'allow' });
export const note = (message) => ({ kind: 'note', message });
export const ask = (message) => ({ kind: 'ask', message });
export const deny = (message) => ({ kind: 'deny', message });

// Normalize whatever a handler returned: nothing, a string (context for the agent) or a result.
export function toResult(out) {
  if (!out) return allow();
  if (typeof out === 'string') return note(out);
  if (typeof out === 'object' && typeof out.kind === 'string') return out;
  return allow();
}

const json = (o) => JSON.stringify(o);

function claude({ kind, message }, event) {
  const text = message ?? '';
  const pre = event === 'PreToolUse';
  if (kind === 'allow') return { stdout: '', stderr: '', exitCode: 0 };
  if (kind === 'note') {
    if (event === 'SessionStart') return { stdout: text, stderr: '', exitCode: 0 };
    if (pre || event === 'PostToolUse' || event === 'UserPromptSubmit') {
      return { stdout: json({ hookSpecificOutput: { hookEventName: event, additionalContext: text } }), stderr: '', exitCode: 0 };
    }
    return { stdout: json({ systemMessage: text }), stderr: '', exitCode: 0 };
  }
  if (pre) {
    const permissionDecision = kind === 'deny' ? 'deny' : 'ask';
    return {
      stdout: json({ hookSpecificOutput: { hookEventName: event, permissionDecision, permissionDecisionReason: text } }),
      stderr: '',
      exitCode: 0,
    };
  }
  if (kind === 'ask') return { stdout: json({ systemMessage: text }), stderr: '', exitCode: 0 };
  return { stdout: json({ decision: 'block', reason: text }), stderr: '', exitCode: 0 };
}

function cursor({ kind, message }, event) {
  const text = message ?? '';
  const before = /^before/i.test(event ?? '');
  if (kind === 'allow') return { stdout: json(before ? { permission: 'allow' } : { continue: true }), stderr: '', exitCode: 0 };
  if (kind === 'note') {
    return before
      ? { stdout: json({ permission: 'allow', agent_message: text }), stderr: '', exitCode: 0 }
      : { stdout: json({ continue: true }), stderr: `${text}\n`, exitCode: 0 };
  }
  if (kind === 'ask') return { stdout: json({ permission: 'ask', user_message: text, agent_message: text }), stderr: '', exitCode: 0 };
  return { stdout: json({ permission: 'deny', user_message: text, agent_message: text }), stderr: `${text}\n`, exitCode: 2 };
}

const RENDERERS = { claude, cursor };
export const RUNTIMES = Object.keys(RENDERERS);

export function render(result, { runtime = 'claude', event } = {}) {
  return (RENDERERS[runtime] ?? claude)(result, event);
}
