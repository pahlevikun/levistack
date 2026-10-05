import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { lintPath } from '../skills/agent-authoring/create-agent/scripts/lint.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const codes = (r, severity) => r.findings.filter((f) => !severity || f.severity === severity).map((f) => f.code);

function tree(files) {
  const root = mkdtempSync(join(tmpdir(), 'create-agent-'));
  for (const [rel, content] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, content);
  }
  return root;
}
const done = (root) => rmSync(root, { recursive: true, force: true });

const goodSkill = '---\nname: good-skill\ndescription: "Does a thing. Use when the user asks for the thing."\n---\n\n# Good\n\nSee [ref](references/a.md).\n';

test('a well-formed skill has no findings', () => {
  const root = tree({ 'good-skill/SKILL.md': goodSkill, 'good-skill/references/a.md': '# A\n' });
  try {
    assert.deepEqual(lintPath(join(root, 'good-skill')).findings, []);
  } finally {
    done(root);
  }
});

test('skill: name must match folder and the spec format', () => {
  const root = tree({
    'a-skill/SKILL.md': '---\nname: Other_Name\ndescription: "x. Use when y."\n---\nbody\n',
  });
  try {
    const c = codes(lintPath(join(root, 'a-skill')), 'error');
    assert.ok(c.includes('name-format'));
    assert.ok(c.includes('name-folder'));
  } finally {
    done(root);
  }
});

test('skill: an unquoted ": " in the description is an error because strict parsers skip the skill', () => {
  const root = tree({ 'bad/SKILL.md': '---\nname: bad\ndescription: Use when stuck: do the thing\n---\nbody\n' });
  try {
    assert.ok(codes(lintPath(join(root, 'bad')), 'error').includes('yaml-unquoted'));
  } finally {
    done(root);
  }
});

test('skill: description length, trigger phrase, broken links and unknown fields', () => {
  const root = tree({
    'long/SKILL.md': `---\nname: long\ndescription: "${'x'.repeat(1030)}"\nbogus: 1\n---\nSee [gone](references/gone.md).\n`,
    'plain/SKILL.md': '---\nname: plain\ndescription: "Handles reports."\n---\nbody\n',
  });
  try {
    const long = lintPath(join(root, 'long'));
    assert.ok(codes(long, 'error').includes('description-length'));
    assert.ok(codes(long, 'error').includes('broken-link'));
    assert.ok(codes(long).includes('unknown-field'));
    assert.ok(codes(lintPath(join(root, 'plain')), 'warn').includes('no-trigger'));
  } finally {
    done(root);
  }
});

test('skill: flags oversized bodies, deep reference chains and unreferenced files', () => {
  const root = tree({
    'big/SKILL.md': `---\nname: big\ndescription: "Big. Use when big."\n---\n${'line\n'.repeat(520)}[a](references/a.md)\n`,
    'big/references/a.md': 'see [b](b.md)\n',
    'big/references/b.md': 'end\n',
    'big/references/orphan.md': 'nobody links me\n',
  });
  try {
    const c = codes(lintPath(join(root, 'big')), 'warn');
    assert.ok(c.includes('too-long'));
    assert.ok(c.includes('deep-reference'));
    assert.ok(c.includes('unreferenced-file'));
  } finally {
    done(root);
  }
});

test('skill: a router may link a speciality guide that links its own references, but references may not chain', () => {
  const root = tree({
    'router/SKILL.md': '---\nname: router\ndescription: "Routes. Use when routing."\n---\nSee [guide](specialities/a/GUIDE.md) and [shared](references/shared.md).\n',
    'router/specialities/a/GUIDE.md': 'Read [detail](references/detail.md) and [shared](../../references/shared.md).\n',
    'router/specialities/a/references/detail.md': 'detail\n',
    'router/references/shared.md': 'shared, links [other](other.md)\n',
    'router/references/other.md': 'other\n',
  });
  try {
    const r = lintPath(join(root, 'router'));
    const deep = r.findings.filter((f) => f.code === 'deep-reference');
    assert.equal(deep.length, 1, JSON.stringify(deep));
    assert.match(deep[0].file, /references\/shared\.md$/);
  } finally {
    done(root);
  }
});

test('agent: needs a description with a trigger, a body, and valid names', () => {
  const root = tree({
    'agents/ok.md': '---\nname: ok\ndescription: "Reviews diffs. Use after writing code."\ntools: Read, Grep\n---\nYou review.\n\nDo not edit files.\n',
    'agents/Bad_Name.md': '---\nname: Bad_Name\ndescription: helps\n---\nbody\n',
    'agents/empty.md': '---\nname: empty\ndescription: "Use when needed."\n---\n',
    'agents/README.md': '# not an agent\n',
  });
  try {
    const r = lintPath(root);
    assert.equal(r.items.length, 3);
    assert.deepEqual(r.findings.filter((f) => f.file === 'agents/ok.md'), []);
    const bad = r.findings.filter((f) => f.file === 'agents/Bad_Name.md').map((f) => f.code);
    assert.ok(bad.includes('name-format'));
    assert.ok(bad.includes('no-trigger'));
    assert.ok(r.findings.some((f) => f.file === 'agents/empty.md' && f.code === 'empty-body'));
  } finally {
    done(root);
  }
});

test('agent: warns on a non-Claude tool name, a read-only body with write tools, and unknown fields', () => {
  const root = tree({
    'agents/x.md': '---\nname: x\ndescription: "Use when asked."\ntools: Read, Shell, Edit\nrole: reviewer\n---\nYou are read-only. Do not edit.\n',
  });
  try {
    const c = codes(lintPath(root), 'warn');
    assert.ok(c.includes('tool-name'));
    assert.ok(c.includes('tools-vs-body'));
    assert.ok(c.includes('unknown-field'));
  } finally {
    done(root);
  }
});

test('agent: "Use on ..." counts as a trigger, and "do not edit production code" is not read-only', () => {
  const root = tree({
    'agents/p.md': '---\nname: p\ndescription: "Plans work. Use on any multi-step task."\ntools: Read, Write, Edit\n---\nYou do not edit production code.\n\nDo not spawn agents.\n',
  });
  try {
    assert.deepEqual(lintPath(root).findings, []);
  } finally {
    done(root);
  }
});

test('skill: warns on a first-person description, a reserved word in the name, and an XML tag in the description', () => {
  const root = tree({
    'helper/SKILL.md': '---\nname: helper\ndescription: "I can help you format reports. Use when you need a report."\n---\nbody\n',
    'claude-tools/SKILL.md': '---\nname: claude-tools\ndescription: "Formats reports. Use when asked."\n---\nbody\n',
    'tagged/SKILL.md': '---\nname: tagged\ndescription: "Writes <name>.md files. Use when asked."\n---\nbody\n',
    'fine/SKILL.md': '---\nname: fine\ndescription: "Formats reports. Use when the user asks you to format a report."\n---\nbody\n',
  });
  try {
    assert.ok(codes(lintPath(join(root, 'helper')), 'warn').includes('first-person'));
    assert.ok(codes(lintPath(join(root, 'claude-tools')), 'warn').includes('reserved-name'));
    assert.ok(codes(lintPath(join(root, 'tagged')), 'warn').includes('xml-in-description'));
    assert.deepEqual(lintPath(join(root, 'fine')).findings, []);
  } finally {
    done(root);
  }
});

test('agent: warns when a subagent needs to ask the user, which it cannot', () => {
  const root = tree({
    'agents/asks.md': '---\nname: asks\ndescription: "Gathers needs. Use when starting."\ntools: Read, AskUserQuestion\n---\nAsk the user what they want, then wait for confirmation.\n\nDo not edit.\n',
    'agents/quiet.md': '---\nname: quiet\ndescription: "Reviews diffs. Use after writing code."\ntools: Read\n---\nReview the diff. If an input is missing, stop and list what is missing in the report.\n\nDo not edit.\n',
  });
  try {
    const r = lintPath(root);
    assert.ok(r.findings.some((f) => f.file === 'agents/asks.md' && f.code === 'needs-user'));
    assert.deepEqual(r.findings.filter((f) => f.file === 'agents/quiet.md'), []);
  } finally {
    done(root);
  }
});

test('the skills in this repo that this skill ships are clean', () => {
  for (const dir of ['create-agent', 'create-agents-md', 'create-skill', 'create-rule', 'create-hook', 'create-command', 'convert-as-skill'].map((s) => `skills/agent-authoring/${s}`).concat('skills/engineering/super-verify', 'skills/architecture/super-architecture')) {
    const errors = lintPath(join(repo, dir)).findings.filter((f) => f.severity === 'error' || f.severity === 'warn');
    assert.deepEqual(errors, [], dir);
  }
});

test('linting the agents directory itself finds every agent, and they have no errors', () => {
  const r = lintPath(join(repo, 'agents'));
  assert.ok(r.items.length >= 11, `checked ${r.items.length} agents`);
  assert.deepEqual(r.findings.filter((f) => f.severity === 'error'), []);
});
