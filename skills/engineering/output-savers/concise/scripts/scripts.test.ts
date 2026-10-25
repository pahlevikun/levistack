import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, beforeEach, describe, test } from 'node:test';
import {
  backupPathFor,
  buildCompressPrompt,
  compressFile,
  isSensitivePath,
  splitFrontmatter,
  stripLlmWrapper,
} from './compress.ts';
import { detectFileType, shouldCompress } from './detect.ts';
import { extractCodeBlocks, validateText } from './validate.ts';

const DOC = [
  '# Rules',
  '',
  'You should always make sure to run the tests before you push. See https://example.com/ci for details.',
  '',
  '- Use `npm test` first',
  '- Never edit `dist/app.js` by hand',
  '',
  '```sh',
  'npm test',
  '```',
  '',
].join('\n');

let dir: string;
let oldXdg: string | undefined;

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'ste-compress-'));
  oldXdg = process.env.XDG_DATA_HOME;
  process.env.XDG_DATA_HOME = join(dir, 'xdg');
});

afterEach(() => {
  if (oldXdg === undefined) delete process.env.XDG_DATA_HOME;
  else process.env.XDG_DATA_HOME = oldXdg;
});

describe('detect', () => {
  test('classifies by extension and name', () => {
    assert.equal(detectFileType('notes.md'), 'natural_language');
    assert.equal(detectFileType('app.ts'), 'code');
    assert.equal(detectFileType('config.yaml'), 'config');
    assert.equal(detectFileType('Dockerfile'), 'code');
    assert.equal(detectFileType('CMakeLists.txt'), 'code');
  });

  test('reads extensionless files', () => {
    const prose = join(dir, 'TODO');
    writeFileSync(prose, 'Call the vendor.\nWrite the report.\n');
    assert.equal(detectFileType(prose), 'natural_language');

    const script = join(dir, 'run');
    writeFileSync(script, '#!/bin/sh\necho hi\n');
    assert.equal(detectFileType(script), 'code');

    const json = join(dir, 'data');
    writeFileSync(json, '{"a": 1}');
    assert.equal(detectFileType(json), 'config');
  });

  test('skips backups and missing files', () => {
    const backup = join(dir, 'notes.original.md');
    writeFileSync(backup, 'x');
    assert.equal(shouldCompress(backup), false);
    assert.equal(shouldCompress(join(dir, 'missing.md')), false);
  });
});

describe('helpers', () => {
  test('splitFrontmatter keeps the block verbatim', () => {
    const [fm, body] = splitFrontmatter('---\nname: x\n---\nHello\n');
    assert.equal(fm, '---\nname: x\n---\n');
    assert.equal(body, 'Hello\n');
    assert.deepEqual(splitFrontmatter('No frontmatter'), ['', 'No frontmatter']);
  });

  test('stripLlmWrapper removes only a wrapping fence', () => {
    assert.equal(stripLlmWrapper('```markdown\nHello\n```'), 'Hello');
    assert.equal(stripLlmWrapper('Hello\n```sh\nls\n```'), 'Hello\n```sh\nls\n```');
  });

  test('isSensitivePath refuses secret-like names', () => {
    for (const p of ['/a/.env', '/a/credentials.md', '/a/my-api-key.md', '/home/x/.ssh/notes.md', '/a/id_rsa']) {
      assert.equal(isSensitivePath(p), true, p);
    }
    assert.equal(isSensitivePath('/a/CLAUDE.md'), false);
  });

  test('backups live outside the source directory', () => {
    const p = backupPathFor('/work/project/notes.md');
    assert.ok(p.startsWith(join(dir, 'xdg', 'ste-compress', 'backups', 'project')));
    assert.ok(p.endsWith('notes.original.md'));
  });

  test('the compress prompt asks for STE and keeps the rules', () => {
    const prompt = buildCompressPrompt('Text');
    assert.match(prompt, /Simplified Technical English/);
    assert.match(prompt, /20 words/);
    assert.match(prompt, /25 words/);
  });
});

describe('validate', () => {
  test('identical text is valid', () => {
    assert.equal(validateText(DOC, DOC).isValid, true);
  });

  test('a lost URL is an error', () => {
    const r = validateText(DOC, DOC.replace('https://example.com/ci', ''));
    assert.equal(r.isValid, false);
    assert.match(r.errors.join('\n'), /URL mismatch/);
  });

  test('a changed code block is an error', () => {
    const r = validateText(DOC, DOC.replace('npm test\n```', 'npm run test\n```'));
    assert.match(r.errors.join('\n'), /Code blocks/);
  });

  test('a changed heading count is an error', () => {
    const r = validateText(DOC, DOC.replace('# Rules', 'Rules'));
    assert.match(r.errors.join('\n'), /Heading count mismatch/);
  });

  test('lost inline code is an error', () => {
    const r = validateText(DOC, DOC.replace('`dist/app.js`', 'the build output'));
    assert.match(r.errors.join('\n'), /Inline code lost/);
  });

  test('extractCodeBlocks handles nested fences and skips unclosed ones', () => {
    const nested = '````md\n```sh\nls\n```\n````\n';
    assert.equal(extractCodeBlocks(nested).length, 1);
    assert.equal(extractCodeBlocks('```sh\nls\n').length, 0);
  });
});

describe('compressFile', () => {
  const good = async (): Promise<string> =>
    [
      '# Rules',
      '',
      'Run the tests before you push. See https://example.com/ci for details.',
      '',
      '- Use `npm test` first.',
      '- Never edit `dist/app.js` by hand.',
      '',
      '```sh',
      'npm test',
      '```',
      '',
    ].join('\n');

  test('writes the backup, then the compressed file', async () => {
    const file = join(dir, 'CLAUDE.md');
    writeFileSync(file, DOC);
    assert.equal(await compressFile(file, good), true);
    assert.equal(readFileSync(backupPathFor(file), 'utf8'), DOC);
    assert.match(readFileSync(file, 'utf8'), /Run the tests before you push/);
  });

  test('keeps frontmatter verbatim', async () => {
    const file = join(dir, 'MEMORY.md');
    writeFileSync(file, `---\nname: x\n---\n${DOC}`);
    await compressFile(file, good);
    assert.ok(readFileSync(file, 'utf8').startsWith('---\nname: x\n---\n'));
  });

  test('restores the original when validation keeps failing', async () => {
    const file = join(dir, 'bad.md');
    writeFileSync(file, DOC);
    const lossy = async (): Promise<string> => '# Rules\n\nShort.';
    assert.equal(await compressFile(file, lossy), false);
    assert.equal(readFileSync(file, 'utf8'), DOC);
    assert.equal(existsSync(backupPathFor(file)), false);
  });

  test('refuses an empty or identical model answer and leaves no backup', async () => {
    const file = join(dir, 'same.md');
    writeFileSync(file, DOC);
    assert.equal(await compressFile(file, async () => ''), false);
    assert.equal(await compressFile(file, async () => DOC), false);
    assert.equal(existsSync(backupPathFor(file)), false);
  });

  test('does not overwrite an existing backup', async () => {
    const file = join(dir, 'twice.md');
    writeFileSync(file, DOC);
    await compressFile(file, good);
    const after = readFileSync(file, 'utf8');
    assert.equal(await compressFile(file, good), false);
    assert.equal(readFileSync(file, 'utf8'), after);
  });

  test('throws for a sensitive filename before any model call', async () => {
    const file = join(dir, 'secrets.md');
    writeFileSync(file, DOC);
    let called = false;
    await assert.rejects(
      compressFile(file, async () => {
        called = true;
        return 'x';
      }),
      /looks sensitive/,
    );
    assert.equal(called, false);
  });

  test('skips code files without calling the model', async () => {
    const file = join(dir, 'app.ts');
    writeFileSync(file, 'export const a = 1;\n');
    assert.equal(await compressFile(file, async () => assert.fail('model called')), false);
  });
});
