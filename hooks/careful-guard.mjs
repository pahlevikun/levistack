// Ask for confirmation before obviously destructive shell commands. Never blocks outright.
import { allow, ask } from './lib/result.mjs';

export const meta = {
  event: 'PreToolUse',
  matcher: 'Bash',
  description: 'Asks before `rm -rf /`, force-push, `reset --hard`, `git clean -f` and `DROP TABLE`',
};

const RISKY = [
  /\brm\s+-[a-z]*(rf|fr)[a-z]*\s+(\/|~|\$HOME)\/?(\s|$)/i,
  /\bgit\s+push\b.*(--force(?!-with-lease)\b|\s-f\b)/,
  /\bgit\s+reset\s+--hard\b/,
  /\bgit\s+clean\s+-[a-z]*f/,
  /\bdrop\s+(table|database)\b/i,
];

export default function carefulGuard({ input }) {
  const cmd = input.command;
  if (!RISKY.some((re) => re.test(cmd))) return allow();
  return ask(`levistack careful-guard: "${cmd.slice(0, 120)}" looks destructive. Confirm before running.`);
}
