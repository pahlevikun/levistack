#!/usr/bin/env node
/**
 * Compare token counts for an original and its compressed file.
 *
 * Usage:
 *   node benchmark.ts <original> <compressed>
 *   node benchmark.ts <directory>     (compares each .md file with its backup)
 *
 * Counts tokens with js-tiktoken (o200k_base) when it is installed.
 * Otherwise it counts words, which is only a rough guide.
 */

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, extname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { backupPathFor } from './compress.ts';
import { validate } from './validate.ts';

type Counter = (text: string) => number;
type Row = [name: string, original: number, compressed: number, savedPercent: number, valid: boolean];

async function loadCounter(): Promise<{ count: Counter; exact: boolean }> {
  try {
    const mod = (await import('js-tiktoken' as string)) as { getEncoding: (n: string) => { encode: (t: string) => unknown[] } };
    const enc = mod.getEncoding('o200k_base');
    return { count: (t) => enc.encode(t).length, exact: true };
  } catch {
    return { count: (t) => t.split(/\s+/).filter(Boolean).length, exact: false };
  }
}

export function benchmarkPair(origPath: string, compPath: string, count: Counter): Row {
  const orig = count(readFileSync(origPath, 'utf8'));
  const comp = count(readFileSync(compPath, 'utf8'));
  const saved = orig > 0 ? (100 * (orig - comp)) / orig : 0;
  return [basename(compPath), orig, comp, saved, validate(origPath, compPath).isValid];
}

function printTable(rows: Row[]): void {
  console.log('\n| File | Original | Compressed | Saved % | Valid |');
  console.log('|------|----------|------------|---------|-------|');
  for (const r of rows) console.log(`| ${r[0]} | ${r[1]} | ${r[2]} | ${r[3].toFixed(1)}% | ${r[4] ? '✅' : '❌'} |`);
}

async function main(argv: string[]): Promise<number> {
  const { count, exact } = await loadCounter();
  if (!exact) console.log('Note: js-tiktoken not installed. Counting words, not tokens.');

  if (argv.length === 2) {
    const [orig, comp] = argv.map((p) => resolve(p));
    for (const p of [orig, comp]) {
      if (!existsSync(p)) {
        console.log(`❌ Not found: ${p}`);
        return 1;
      }
    }
    printTable([benchmarkPair(orig, comp, count)]);
    return 0;
  }

  if (argv.length === 1 && existsSync(argv[0]) && statSync(argv[0]).isDirectory()) {
    const dir = resolve(argv[0]);
    const rows: Row[] = [];
    for (const name of readdirSync(dir).sort()) {
      if (extname(name) !== '.md' || name.endsWith('.original.md')) continue;
      const comp = join(dir, name);
      const orig = backupPathFor(comp);
      if (existsSync(orig)) rows.push(benchmarkPair(orig, comp, count));
    }
    if (!rows.length) {
      console.log('No compressed files with backups found.');
      return 0;
    }
    printTable(rows);
    return 0;
  }

  console.log('Usage: node benchmark.ts <original> <compressed>  or  node benchmark.ts <directory>');
  return 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = await main(process.argv.slice(2));
}
