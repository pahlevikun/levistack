// Protect the context budget: block untargeted full reads of big files, and redirect to the bulk-reader agent.
// Targeted reads (offset/limit) and piped/filtered shell commands always pass. Ambiguous input fails open.
import { countLines, isFile, resolveFrom } from './lib/files.mjs';
import { logEvent } from './lib/metrics.mjs';
import { allow, deny } from './lib/result.mjs';

export const meta = {
  event: 'PreToolUse',
  matcher: 'Read|Bash',
  description: 'Blocks full reads of files over 350 lines (Read, or bare cat/head/tail/less/more) and points to `bulk-reader`',
};

const DUMP_VERBS = new Set(['cat', 'head', 'tail', 'less', 'more']);
// Anything that already narrows the output is a targeted read, not a dump.
const NARROWED = /\||>|\s-n\s|grep|sed|awk/;

const maxLines = () => Number(process.env.LEVISTACK_MAX_READ_LINES) || 350;

function gate({ hook, label, file, redirect }) {
  if (!isFile(file)) return allow();
  const lines = countLines(file);
  const limit = maxLines();
  if (lines <= limit) return allow();
  logEvent(hook, { decision: 'block', file, lines });
  return deny(`${label(lines, limit)} Blocked to protect the context budget. ${redirect}`);
}

export default function largeReadGuard({ input }) {
  const { tool, command, filePath, offset, limit, cwd } = input;

  if (tool === 'Read' || (!tool && !command && filePath)) {
    if (offset != null || limit != null) return allow();
    return gate({
      hook: 'large-read-guard',
      file: filePath && resolveFrom(cwd, filePath),
      label: (lines, max) => `${filePath} is ${lines} lines (> ${max}).`,
      redirect: 'Delegate to the `bulk-reader` agent with the path and your question, or re-read with offset/limit for the exact section.',
    });
  }

  if ((tool === 'Bash' || !tool) && command && !NARROWED.test(command)) {
    const tokens = command.trim().split(/\s+/);
    if (!DUMP_VERBS.has(tokens[0])) return allow();
    const file = tokens.at(-1).replace(/["']/g, '');
    return gate({
      hook: 'large-read-guard',
      file: file && resolveFrom(cwd, file),
      label: (lines, max) => `'${tokens[0]} ${file}' dumps ${lines} lines (> ${max}).`,
      redirect: 'Delegate to the `bulk-reader` agent, or use sed -n / head -c for a targeted slice.',
    });
  }
  return allow();
}
