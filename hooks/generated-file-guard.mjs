// Ask before editing generated output: files whose header says "do not edit", and coverage artifacts.
import { basename } from 'node:path';
import { isFile, readHead, resolveFrom } from './lib/files.mjs';
import { allow, ask } from './lib/result.mjs';

export const meta = {
  event: 'PreToolUse',
  matcher: 'Write|Edit|MultiEdit',
  description: 'Asks before editing files marked generated ("do not edit", `@generated`) or writing coverage artifacts',
};

const HEADER_LINES = 5;
const GENERATED_HEADER = /@generated\b|\bdo not edit\b|\bgenerated (by|file|code)\b/i;
const COVERAGE_ARTIFACT = /^(coverage.*\.(out|txt|xml|json)|lcov\.info|\.coverage)$/;

export default function generatedFileGuard({ input }) {
  const { filePath, cwd } = input;
  if (!filePath) return allow();

  if (COVERAGE_ARTIFACT.test(basename(filePath))) {
    return ask(`levistack generated-file-guard: ${filePath} is a generated coverage artifact. Do not write or commit it by hand.`);
  }

  const abs = resolveFrom(cwd, filePath);
  if (!isFile(abs)) return allow(); // a new file cannot be generated output yet
  const header = readHead(abs).split('\n', HEADER_LINES).join('\n');
  if (GENERATED_HEADER.test(header)) {
    return ask(`levistack generated-file-guard: ${filePath} looks generated (its header says so). Edit the source and regenerate instead.`);
  }
  return allow();
}
