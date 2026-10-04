#!/usr/bin/env node
/** Check that a compressed file kept everything that must survive compression. */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const W = '\\p{L}\\p{N}_';
const URL_RE = /https?:\/\/[^\s)]+/g;
const FENCE_OPEN_RE = /^(\s{0,3})(`{3,}|~{3,})(.*)$/;
const HEADING_RE = /^(#{1,6})\s+(.*)/gm;
const BULLET_RE = /^\s*[-*+]\s+/gm;

// Crude but effective path detection. Needs a path prefix (./ ../ / or a drive letter)
// or a slash or backslash inside the match.
const PATH_RE = new RegExp(
  `(?:\\./|\\.\\./|/|[A-Za-z]:\\\\)[${W}\\-/\\\\.]+|[${W}\\-.]+[/\\\\][${W}\\-/\\\\.]+`,
  'gu',
);

export class ValidationResult {
  isValid = true;
  errors: string[] = [];
  warnings: string[] = [];

  addError(msg: string): void {
    this.isValid = false;
    this.errors.push(msg);
  }

  addWarning(msg: string): void {
    this.warnings.push(msg);
  }
}

function readText(path: string): string {
  return readFileSync(path, 'utf8');
}

const setDiff = (a: Set<string>, b: Set<string>): string[] => [...a].filter((x) => !b.has(x)).sort();

// ---------- Extractors ----------

export function extractHeadings(text: string): Array<[string, string]> {
  return [...text.matchAll(HEADING_RE)].map((m): [string, string] => [m[1], m[2].trim()]);
}

/**
 * Line-based fenced code block extractor.
 * Handles ``` and ~~~ fences of any length (CommonMark: the closing fence uses the same
 * character and is at least as long as the opening one). Supports nested fences, such as
 * an outer 4-backtick block wrapping inner 3-backtick content.
 */
export function extractCodeBlocks(text: string): string[] {
  const blocks: string[] = [];
  const lines = text.split('\n');
  let i = 0;
  const n = lines.length;
  while (i < n) {
    const m = FENCE_OPEN_RE.exec(lines[i]);
    if (!m) {
      i += 1;
      continue;
    }
    const fenceChar = m[2][0];
    const fenceLen = m[2].length;
    const blockLines = [lines[i]];
    i += 1;
    let closed = false;
    while (i < n) {
      const c = FENCE_OPEN_RE.exec(lines[i]);
      if (c && c[2][0] === fenceChar && c[2].length >= fenceLen && c[3].trim() === '') {
        blockLines.push(lines[i]);
        closed = true;
        i += 1;
        break;
      }
      blockLines.push(lines[i]);
      i += 1;
    }
    // Unclosed fences are skipped. They mean malformed markdown, and counting them
    // would cause false validation failures.
    if (closed) blocks.push(blockLines.join('\n'));
  }
  return blocks;
}

export const extractUrls = (text: string): Set<string> => new Set(text.match(URL_RE) ?? []);
export const extractPaths = (text: string): Set<string> => new Set(text.match(PATH_RE) ?? []);
export const countBullets = (text: string): number => (text.match(BULLET_RE) ?? []).length;

export function extractInlineCodes(text: string): string[] {
  let t = text.replace(/^```[\s\S]*?^```/gm, '');
  t = t.replace(/^~~~[\s\S]*?^~~~/gm, '');
  return [...t.matchAll(/`([^`]+)`/g)].map((m) => m[1]);
}

const countBy = (items: string[]): Map<string, number> => {
  const counts = new Map<string, number>();
  for (const item of items) counts.set(item, (counts.get(item) ?? 0) + 1);
  return counts;
};

// ---------- Validators ----------

function validateHeadings(orig: string, comp: string, result: ValidationResult): void {
  const h1 = extractHeadings(orig);
  const h2 = extractHeadings(comp);
  if (h1.length !== h2.length) result.addError(`Heading count mismatch: ${h1.length} vs ${h2.length}`);
  if (JSON.stringify(h1) !== JSON.stringify(h2)) result.addWarning('Heading text/order changed');
}

function validateCodeBlocks(orig: string, comp: string, result: ValidationResult): void {
  if (JSON.stringify(extractCodeBlocks(orig)) !== JSON.stringify(extractCodeBlocks(comp))) {
    result.addError('Code blocks not preserved exactly');
  }
}

function validateUrls(orig: string, comp: string, result: ValidationResult): void {
  const u1 = extractUrls(orig);
  const u2 = extractUrls(comp);
  const lost = setDiff(u1, u2);
  const added = setDiff(u2, u1);
  if (lost.length || added.length) {
    result.addError(`URL mismatch: lost=${JSON.stringify(lost)}, added=${JSON.stringify(added)}`);
  }
}

function validatePaths(orig: string, comp: string, result: ValidationResult): void {
  const p1 = extractPaths(orig);
  const p2 = extractPaths(comp);
  const lost = setDiff(p1, p2);
  const added = setDiff(p2, p1);
  if (lost.length || added.length) {
    result.addWarning(`Path mismatch: lost=${JSON.stringify(lost)}, added=${JSON.stringify(added)}`);
  }
}

function validateBullets(orig: string, comp: string, result: ValidationResult): void {
  const b1 = countBullets(orig);
  const b2 = countBullets(comp);
  if (b1 === 0) return;
  if (Math.abs(b1 - b2) / b1 > 0.15) result.addWarning(`Bullet count changed too much: ${b1} -> ${b2}`);
}

function validateInlineCodes(orig: string, comp: string, result: ValidationResult): void {
  const c1 = countBy(extractInlineCodes(orig));
  const c2 = countBy(extractInlineCodes(comp));
  const lost = new Set<string>();
  const added = new Set<string>();
  for (const [code, count] of c1) {
    const other = c2.get(code);
    if (other === undefined) lost.add(code);
    else if (other < count) lost.add(`${code} (lost ${count - other} of ${count} occurrences)`);
  }
  for (const code of c2.keys()) if (!c1.has(code)) added.add(code);
  if (lost.size) result.addError(`Inline code lost: ${JSON.stringify([...lost].sort())}`);
  if (added.size) result.addWarning(`Inline code added: ${JSON.stringify([...added].sort())}`);
}

// ---------- Main ----------

/** Validate the text of a compressed file against its original. */
export function validateText(orig: string, comp: string): ValidationResult {
  const result = new ValidationResult();
  validateHeadings(orig, comp, result);
  validateCodeBlocks(orig, comp, result);
  validateUrls(orig, comp, result);
  validatePaths(orig, comp, result);
  validateBullets(orig, comp, result);
  validateInlineCodes(orig, comp, result);
  return result;
}

export function validate(originalPath: string, compressedPath: string): ValidationResult {
  return validateText(readText(originalPath), readText(compressedPath));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.length !== 4) {
    console.log('Usage: node validate.ts <original> <compressed>');
    process.exit(1);
  }
  const res = validate(resolve(process.argv[2]), resolve(process.argv[3]));
  console.log(`\nValid: ${res.isValid}`);
  if (res.errors.length) console.log(`\nErrors:\n${res.errors.map((e) => `  - ${e}`).join('\n')}`);
  if (res.warnings.length) console.log(`\nWarnings:\n${res.warnings.map((w) => `  - ${w}`).join('\n')}`);
}
