#!/usr/bin/env node
/**
 * Compress a memory or instruction file into STE.
 *
 * Usage: node cli.ts <filepath>
 * Needs Node 22.18 or later (native TypeScript). On 22.6 to 22.17 add --experimental-strip-types.
 * Exit codes: 0 done or skipped, 1 usage or error, 2 compression failed, 130 interrupted.
 */

import { existsSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { backupPathFor, compressFile } from './compress.ts';
import { detectFileType, shouldCompress } from './detect.ts';

function usage(): void {
  console.log('Usage: node cli.ts <filepath>');
}

export async function main(argv: string[]): Promise<number> {
  if (argv.length !== 1) {
    usage();
    return 1;
  }

  const input = argv[0];
  if (!existsSync(input)) {
    console.log(`❌ File not found: ${input}`);
    return 1;
  }
  if (!statSync(input).isFile()) {
    console.log(`❌ Not a file: ${input}`);
    return 1;
  }

  const filepath = resolve(input);
  console.log(`Detected: ${detectFileType(filepath)}`);

  if (!shouldCompress(filepath)) {
    console.log('Skipping: file is not natural language (code/config)');
    return 0;
  }

  console.log('Starting STE compression...\n');

  try {
    if (await compressFile(filepath)) {
      console.log('\nCompression completed successfully');
      console.log(`Compressed: ${filepath}`);
      console.log(`Original:   ${backupPathFor(filepath)}`);
      return 0;
    }
    console.log('\n❌ Compression failed or was refused');
    return 2;
  } catch (e) {
    console.log(`\n❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    return 1;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.on('SIGINT', () => {
    console.log('\nInterrupted by user');
    process.exit(130);
  });
  process.exitCode = await main(process.argv.slice(2));
}
