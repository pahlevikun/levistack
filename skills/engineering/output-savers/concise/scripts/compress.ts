#!/usr/bin/env node
/**
 * Memory file compression orchestrator.
 *
 * Rewrites a natural language markdown file in Simplified Technical English (STE)
 * to cut input tokens. Code, URLs, paths, and headings stay byte for byte.
 *
 * Usage: node compress.ts <filepath>
 */

import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, delimiter, dirname, extname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { shouldCompress } from './detect.ts';
import { validate } from './validate.ts';

export const MAX_RETRIES = 2;
const MAX_FILE_SIZE = 500_000; // 500 KB
const DEFAULT_MODEL = 'claude-sonnet-5-5';

const OUTER_FENCE_RE = /^\s*(`{3,}|~{3,})[^\n]*\n([\s\S]*)\n\1\s*$/;

// YAML frontmatter: starts at the first line with --- and ends at the next --- line.
// Captures the whole block (delimiters and trailing newline) and the body after it.
const FRONTMATTER_RE = /^(---\r?\n[\s\S]*?\r?\n---\r?\n)([\s\S]*)/;

/**
 * Filenames that almost certainly hold secrets or PII. Compressing ships the raw bytes
 * to the Anthropic API, a third-party boundary. detect.ts already skips .env by extension,
 * but credentials.md or secrets.txt would pass the natural language filter.
 * This is a hard refusal before any read.
 */
const SENSITIVE_BASENAME_RE = new RegExp(
  '^(' +
    [
      String.raw`\.env(\..+)?`,
      String.raw`\.netrc`,
      String.raw`credentials(\..+)?`,
      String.raw`secrets?(\..+)?`,
      String.raw`passwords?(\..+)?`,
      String.raw`id_(rsa|dsa|ecdsa|ed25519)(\.pub)?`,
      'authorized_keys',
      'known_hosts',
      String.raw`.*\.(pem|key|p12|pfx|crt|cer|jks|keystore|asc|gpg)`,
    ].join('|') +
    ')$',
  'i',
);

const SENSITIVE_PATH_COMPONENTS = new Set(['.ssh', '.aws', '.gnupg', '.kube', '.docker']);

const SENSITIVE_NAME_TOKENS = ['secret', 'credential', 'password', 'passwd', 'apikey', 'accesskey', 'token', 'privatekey'];

/** Split YAML frontmatter from the body. Returns [frontmatter, body]. */
export function splitFrontmatter(text: string): [string, string] {
  const m = FRONTMATTER_RE.exec(text);
  return m ? [m[1], m[2]] : ['', text];
}

/** Strip an outer ``` fence when it wraps the whole model output. */
export function stripLlmWrapper(text: string): string {
  const m = OUTER_FENCE_RE.exec(text);
  return m ? m[2] : text;
}

/**
 * Backups live OUTSIDE the source directory, so rule and instruction loaders
 * do not read the `.original.md` copy as a live file.
 *   Windows: %LOCALAPPDATA%\ste-compress\backups
 *   Other:   $XDG_DATA_HOME/ste-compress/backups, or ~/.local/share/ste-compress/backups
 * The parent directory name of the source is mirrored below the base to avoid
 * collisions between two `task.md` files in different projects.
 */
export function backupDirFor(filepath: string): string {
  let base: string;
  if (process.platform === 'win32') {
    base = join(process.env.LOCALAPPDATA || join(homedir(), 'AppData', 'Local'), 'ste-compress', 'backups');
  } else {
    base = join(process.env.XDG_DATA_HOME || join(homedir(), '.local', 'share'), 'ste-compress', 'backups');
  }
  return join(base, basename(dirname(filepath)));
}

export function backupPathFor(filepath: string): string {
  const stem = basename(filepath, extname(filepath));
  return join(backupDirFor(filepath), `${stem}.original.md`);
}

/** Heuristic denylist for files that must never go to a third-party API. */
export function isSensitivePath(filepath: string): boolean {
  if (SENSITIVE_BASENAME_RE.test(basename(filepath))) return true;
  if (filepath.split(/[\\/]+/).some((part) => SENSITIVE_PATH_COMPONENTS.has(part.toLowerCase()))) return true;
  // Normalize separators so "api-key" and "api_key" both match "apikey".
  const lower = basename(filepath).toLowerCase().replace(/[_\-\s.]/g, '');
  return SENSITIVE_NAME_TOKENS.some((tok) => lower.includes(tok));
}

// ---------- Model calls ----------

function findOnPath(cmd: string): string {
  const exts = process.platform === 'win32' ? (process.env.PATHEXT || '.EXE;.CMD;.BAT').split(';') : [''];
  for (const dir of (process.env.PATH || '').split(delimiter)) {
    for (const ext of exts) {
      const candidate = join(dir, cmd + ext);
      if (existsSync(candidate) && statSync(candidate).isFile()) return candidate;
    }
  }
  return cmd;
}

export type ModelCall = (prompt: string) => Promise<string>;

/**
 * Send a prompt to Claude.
 * With ANTHROPIC_API_KEY set, call the Messages API over HTTPS. Otherwise run
 * `claude --print` (which uses the desktop login). No shell is involved: the prompt
 * goes through stdin and the argument list is fixed.
 * On Windows the CLI is often a .cmd shim that Node cannot start without a shell,
 * so set ANTHROPIC_API_KEY there.
 */
export const callClaude: ModelCall = async (prompt) => {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (apiKey) {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({
        model: process.env.STE_COMPRESS_MODEL || DEFAULT_MODEL,
        max_tokens: 8192,
        messages: [{ role: 'user', content: prompt }],
      }),
    });
    if (!res.ok) throw new Error(`Anthropic API error ${res.status}: ${await res.text()}`);
    const data = (await res.json()) as { content?: Array<{ type: string; text?: string }> };
    const text = data.content?.find((b) => b.type === 'text')?.text ?? '';
    return stripLlmWrapper(text.trim());
  }

  const result = spawnSync(findOnPath('claude'), ['--print'], {
    input: prompt,
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) {
    throw new Error(`Cannot run the claude CLI (${result.error.message}). Install Claude Code or set ANTHROPIC_API_KEY.`);
  }
  if (result.status !== 0) throw new Error(`Claude call failed:\n${result.stderr}`);
  return stripLlmWrapper(result.stdout.trim());
};

export function buildCompressPrompt(original: string): string {
  return `
Rewrite this markdown in Simplified Technical English (STE) to save tokens.

STRICT RULES:
- Do NOT change anything inside \`\`\` code blocks.
- Do NOT change anything inside inline backticks.
- Keep ALL URLs exactly.
- Keep ALL headings exactly.
- Keep file paths, commands, numbers, dates, and version strings exactly.
- Keep every negation and condition ("do not", "never", "only if", "unless").
- Write short, active sentences with one idea each. Use at most 20 words in an instruction and at most 25 words in a description.
- Remove filler, praise, hedging, and repeated points. Keep the articles (a, an, the). Do not write fragments.
- Use one word for one meaning. Keep each technical term the same everywhere.
- Return ONLY the rewritten markdown body. Do NOT wrap the whole output in a \`\`\`markdown fence or any other fence. Inner code blocks from the original stay as they are. Do not add a new outer fence around the whole file.

Only rewrite natural language.

TEXT:
${original}
`;
}

export function buildFixPrompt(original: string, compressed: string, errors: string[]): string {
  const errorsText = errors.map((e) => `- ${e}`).join('\n');
  return `You are fixing an STE-compressed markdown file. Specific validation errors were found.

CRITICAL RULES:
- DO NOT recompress or rephrase the file.
- ONLY fix the listed errors. Leave everything else exactly as it is.
- The ORIGINAL is provided as reference only (to restore missing content).
- Keep the STE style in all untouched sections.

ERRORS TO FIX:
${errorsText}

HOW TO FIX:
- Missing URL: find it in ORIGINAL, restore it exactly where it belongs in COMPRESSED.
- Code block mismatch: find the exact code block in ORIGINAL, restore it in COMPRESSED.
- Heading mismatch: restore the exact heading text from ORIGINAL into COMPRESSED.
- Do not touch any section not mentioned in the errors.

ORIGINAL (reference only):
${original}

COMPRESSED (fix this):
${compressed}

Return ONLY the fixed compressed file. No explanation.
`;
}

// ---------- Core logic ----------

/**
 * Compress one file. Returns true on success and false on a safe refusal or failure
 * (the original file is left as it was). Throws on bad input or a failed model call.
 * `call` is injectable so tests run without a network.
 */
export async function compressFile(filepath: string, call: ModelCall = callClaude): Promise<boolean> {
  filepath = resolve(filepath);
  if (!existsSync(filepath)) throw new Error(`File not found: ${filepath}`);
  if (statSync(filepath).size > MAX_FILE_SIZE) {
    throw new Error(`File too large to compress safely (max 500KB): ${filepath}`);
  }

  // Refuse files that look like secrets. Compression sends the raw bytes to the
  // Anthropic API. The user must rename the file if the heuristic is wrong.
  if (isSensitivePath(filepath)) {
    throw new Error(
      `Refusing to compress ${filepath}: filename looks sensitive ` +
        '(credentials, keys, secrets, or known private paths). ' +
        'Compression sends file contents to the Anthropic API. ' +
        'Rename the file if this is a false positive.',
    );
  }

  console.log(`Processing: ${filepath}`);

  if (!shouldCompress(filepath)) {
    console.log('Skipping (not natural language)');
    return false;
  }

  const originalText = readFileSync(filepath, 'utf8');
  const backupPath = backupPathFor(filepath);
  mkdirSync(dirname(backupPath), { recursive: true });

  if (!originalText.trim()) {
    console.log('❌ Refusing to compress: file is empty or whitespace-only.');
    return false;
  }

  // Never overwrite an existing backup. It may hold the only copy of the original.
  if (existsSync(backupPath)) {
    console.log(`⚠️ Backup file already exists: ${backupPath}`);
    console.log('The original backup may contain important content.');
    console.log('Aborting to prevent data loss. Remove or rename the backup file to proceed.');
    return false;
  }

  // Keep frontmatter verbatim: remove it from the input and put it back on the output.
  const [frontmatter, body] = splitFrontmatter(originalText);
  if (frontmatter) console.log(`Detected YAML frontmatter (${frontmatter.length} chars), preserving verbatim`);

  if (!body.trim()) {
    console.log('❌ Refusing to compress: body is empty after frontmatter removal.');
    return false;
  }

  // Step 1: compress the body only.
  console.log('Compressing with Claude...');
  const compressedBody = await call(buildCompressPrompt(body));

  if (!compressedBody || !compressedBody.trim()) {
    console.log('❌ Compression aborted: Claude returned an empty response.');
    console.log('   Original file is untouched (no backup created).');
    return false;
  }

  // Judge identity on the body. The frontmatter never changes.
  if (compressedBody.trim() === body.trim()) {
    console.log('❌ Compression aborted: output is identical to input.');
    console.log('   Likely causes: Claude refused, returned the prompt unchanged, or the file is');
    console.log('   already compact. Original file is untouched (no backup created).');
    return false;
  }

  let compressed = frontmatter + compressedBody;

  // Write the backup and read it back before touching the input file. If the disk
  // dropped bytes, remove the bad backup and stop.
  writeFileSync(backupPath, originalText, 'utf8');
  if (readFileSync(backupPath, 'utf8') !== originalText) {
    console.log(`❌ Backup write verification failed: ${backupPath}`);
    console.log('   In-memory original differs from on-disk backup. Aborting before touching the input file.');
    rmSync(backupPath, { force: true });
    return false;
  }
  writeFileSync(filepath, compressed, 'utf8');

  // Step 2: validate, with targeted fixes.
  for (let attempt = 0; attempt < MAX_RETRIES; attempt += 1) {
    console.log(`\nValidation attempt ${attempt + 1}`);
    const result = validate(backupPath, filepath);

    if (result.isValid) {
      console.log('Validation passed');
      return true;
    }

    console.log('❌ Validation failed:');
    for (const err of result.errors) console.log(`   - ${err}`);

    if (attempt === MAX_RETRIES - 1) {
      writeFileSync(filepath, originalText, 'utf8');
      rmSync(backupPath, { force: true });
      console.log('❌ Failed after retries, original restored');
      return false;
    }

    console.log('Fixing with Claude...');
    compressed = await call(buildFixPrompt(originalText, compressed, result.errors));
    writeFileSync(filepath, compressed, 'utf8');
  }

  return true;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  console.log('Use cli.ts: node cli.ts <filepath>');
  process.exit(1);
}

