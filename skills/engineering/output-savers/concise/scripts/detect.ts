#!/usr/bin/env node
/** Detect whether a file is natural language (compressible) or code/config (skip). */

import { readFileSync, statSync } from 'node:fs';
import { basename, extname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

export type FileType = 'natural_language' | 'code' | 'config' | 'unknown';

/** Extensions that are natural language and compressible. */
export const COMPRESSIBLE_EXTENSIONS = new Set(['.md', '.txt', '.markdown', '.rst', '.typ', '.typst', '.tex']);

/** Extensions that are code or config and must be skipped. */
export const SKIP_EXTENSIONS = new Set([
  '.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yaml', '.yml',
  '.toml', '.env', '.lock', '.css', '.scss', '.html', '.xml',
  '.sql', '.sh', '.bash', '.zsh', '.go', '.rs', '.java', '.c',
  '.cpp', '.h', '.hpp', '.rb', '.php', '.swift', '.kt', '.lua',
  '.dockerfile', '.makefile', '.csv', '.ini', '.cfg',
]);

const CONFIG_EXTENSIONS = new Set(['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env']);

/**
 * Well-known build and config files with no extension, or a misleading one.
 * `Dockerfile` has no suffix, and `CMakeLists.txt` would ride the compressible `.txt` rule.
 * Checked by basename before any extension rule.
 */
export const KNOWN_CODE_FILENAMES = new Set([
  'dockerfile', 'makefile', 'gnumakefile', 'jenkinsfile', 'vagrantfile',
  'rakefile', 'gemfile', 'justfile', 'procfile', 'brewfile',
  'cmakelists.txt',
]);

/** Patterns that indicate a line is code. */
const CODE_PATTERNS: RegExp[] = [
  /^\s*(import |from .+ import |require\(|const |let |var )/,
  /^\s*(def |class |function |async function |export )/,
  /^\s*(if\s*\(|for\s*\(|while\s*\(|switch\s*\(|try\s*\{)/,
  /^\s*[}\]);]+\s*$/, // closing braces and brackets
  /^\s*@\w+/, // decorators and annotations
  /^\s*"[^"]+"\s*:\s*/, // JSON-like key and value
  /^\s*\w+\s*=\s*[{[("']/, // assignment with a literal
];

function isCodeLine(line: string): boolean {
  return CODE_PATTERNS.some((p) => p.test(line));
}

function isJsonContent(text: string): boolean {
  try {
    JSON.parse(text);
    return true;
  } catch {
    return false;
  }
}

/** Heuristic: does the content look like YAML? */
function isYamlContent(lines: string[]): boolean {
  let indicators = 0;
  const head = lines.slice(0, 30);
  for (const line of head) {
    const stripped = line.trim();
    if (stripped.startsWith('---')) indicators += 1;
    else if (/^\w[\w\s]*:\s/.test(stripped)) indicators += 1;
    else if (stripped.startsWith('- ') && stripped.includes(':')) indicators += 1;
  }
  const nonEmpty = head.filter((l) => l.trim()).length;
  return nonEmpty > 0 && indicators / nonEmpty > 0.6;
}

/** Classify a file as 'natural_language', 'code', 'config', or 'unknown'. */
export function detectFileType(filepath: string): FileType {
  const ext = extname(filepath).toLowerCase();

  // Known code filenames win over any extension rule.
  if (KNOWN_CODE_FILENAMES.has(basename(filepath).toLowerCase())) return 'code';

  if (COMPRESSIBLE_EXTENSIONS.has(ext)) return 'natural_language';
  if (SKIP_EXTENSIONS.has(ext)) return CONFIG_EXTENSIONS.has(ext) ? 'config' : 'code';

  // Extensionless files (CLAUDE.md-style notes, TODO): look at the content.
  if (!ext) {
    let text: string;
    try {
      text = readFileSync(filepath, 'utf8');
    } catch {
      return 'unknown';
    }

    // A shebang means an executable script, never prose.
    if (text.startsWith('#!')) return 'code';

    const lines = text.split(/\r?\n/).slice(0, 50);
    if (isJsonContent(text.slice(0, 10000))) return 'config';
    if (isYamlContent(lines)) return 'config';

    const nonEmpty = lines.filter((l) => l.trim()).length;
    const codeLines = lines.filter((l) => l.trim() && isCodeLine(l)).length;
    if (nonEmpty > 0 && codeLines / nonEmpty > 0.4) return 'code';

    return 'natural_language';
  }

  return 'unknown';
}

/** True when the file is natural language and should be compressed. */
export function shouldCompress(filepath: string): boolean {
  try {
    if (!statSync(filepath).isFile()) return false;
  } catch {
    return false;
  }
  // Skip backup files.
  if (basename(filepath).endsWith('.original.md')) return false;
  return detectFileType(filepath) === 'natural_language';
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const files = process.argv.slice(2);
  if (files.length === 0) {
    console.log('Usage: node detect.ts <file1> [file2] ...');
    process.exit(1);
  }
  for (const f of files) {
    const p = resolve(f);
    console.log(`  ${basename(p).padEnd(30)} type=${detectFileType(p).padEnd(20)} compress=${shouldCompress(p)}`);
  }
}
