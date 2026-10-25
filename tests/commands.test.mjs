import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const commandsDir = join(root, 'commands');
const files = readdirSync(commandsDir).filter((f) => f.endsWith('.md'));

function skillNames() {
  const names = new Set();
  for (const group of readdirSync(join(root, 'skills'), { withFileTypes: true })) {
    if (!group.isDirectory()) continue;
    for (const s of readdirSync(join(root, 'skills', group.name), { withFileTypes: true })) {
      if (s.isDirectory() && existsSync(join(root, 'skills', group.name, s.name, 'SKILL.md'))) names.add(s.name);
    }
  }
  return names;
}

function parse(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  assert.ok(m, 'a command starts with frontmatter');
  const fm = Object.fromEntries(m[1].split('\n').map((l) => [l.slice(0, l.indexOf(':')), l.slice(l.indexOf(':') + 1).trim()]));
  return { fm, body: m[2].trim() };
}

test('there are at least a dozen commands', () => {
  assert.ok(files.length >= 12, `only ${files.length} commands`);
});

test('every command: one quoted description line, an argument hint when it reads arguments, short body', () => {
  for (const f of files) {
    const { fm, body } = parse(readFileSync(join(commandsDir, f), 'utf8'));
    assert.match(fm.description, /^".+"$/, `${f}: description must be one quoted line`);
    assert.ok(fm.description.length <= 200, `${f}: description is too long for the / menu`);
    if (body.includes('$ARGUMENTS')) assert.ok(fm['argument-hint'], `${f}: reads $ARGUMENTS but has no argument-hint`);
    assert.ok(body.split('\n').length <= 20, `${f}: body is over 20 lines. Point to the skill for the method`);
    assert.doesNotMatch(body, /[—–;]/, `${f}: no em dash, en dash or semicolon in prose`);
  }
});

test('every command names a skill that exists, and states what it must not do', () => {
  const skills = skillNames();
  for (const f of files) {
    const body = readFileSync(join(commandsDir, f), 'utf8');
    const named = [...skills].filter((s) => new RegExp(`\\b${s}\\b`).test(body));
    assert.ok(named.length >= 1, `${f}: names no skill from the catalog`);
    assert.match(body, /\bDo not\b/, `${f}: add a guardrail ("Do not ...")`);
  }
});

test('no command carries an upstream name or a personal path', () => {
  for (const f of files) {
    const body = readFileSync(join(commandsDir, f), 'utf8');
    assert.doesNotMatch(body, /\/Users\/|github\.com\/|skills\.sh/, `${f}: no personal path or upstream link in a shipped command`);
  }
});
