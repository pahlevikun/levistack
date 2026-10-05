import assert from 'node:assert/strict';
import { test } from 'node:test';
import { checkRule } from '../skills/agent-authoring/create-rule/scripts/check-rule.mjs';
import { buildPayload, interpret } from '../skills/agent-authoring/create-hook/scripts/try-hook.mjs';
import { convertSource, slugify } from '../skills/agent-authoring/convert-as-skill/scripts/convert.mjs';

const codes = (findings, severity) => findings.filter((f) => !severity || f.severity === severity).map((f) => f.code);

// check-rule
test('check-rule: an unquoted leading * in globs is a YAML error', () => {
  const f = checkRule('x.mdc', '---\nglobs: *.ts\nalwaysApply: false\n---\nbody\n');
  assert.ok(codes(f, 'error').includes('yaml-leading-indicator'));
});

test('check-rule: a quoted, scoped rule is clean', () => {
  assert.deepEqual(checkRule('x.mdc', '---\ndescription: "TS rules"\nglobs: "**/*.ts"\nalwaysApply: false\n---\n- Do x.\n'), []);
});

test('check-rule: warns when a Cursor rule can never apply, and when scope fields conflict', () => {
  assert.ok(codes(checkRule('x.mdc', '---\nalwaysApply: false\n---\nbody\n')).includes('never-applies'));
  assert.ok(codes(checkRule('x.md', '---\ndescription: "d"\nalwaysApply: true\nglobs: "*.ts"\n---\nbody\n')).includes('scope-conflict'));
});

test('check-rule: Claude Code rules only read paths; empty bodies are errors', () => {
  const f = checkRule('/p/.claude/rules/a.md', '---\ndescription: "d"\npaths:\n  - "src/**"\n---\nbody\n');
  assert.ok(codes(f).includes('ignored-field'));
  assert.ok(codes(checkRule('y.md', '---\ndescription: "d"\nalwaysApply: false\n---\n\n'), 'error').includes('empty-body'));
});

test('check-rule: flags hedged wording outside code, and leaves a firm rule alone', () => {
  const hedged = checkRule('x.md', '---\ndescription: "d"\nalwaysApply: true\n---\nTry to keep functions short. Generally prefer early returns.\n');
  assert.ok(codes(hedged, 'info').includes('hedged-language'));
  assert.match(hedged.find((f) => f.code === 'hedged-language').message, /try to/);
  const firm = checkRule('x.md', '---\ndescription: "d"\nalwaysApply: true\n---\nKeep functions under 40 lines, except generated code.\n\n```\n// try to read this\n```\n');
  assert.ok(!codes(firm).includes('hedged-language'));
});

// try-hook
test('try-hook: builds a Claude Code tool payload', () => {
  const p = buildPayload({ event: 'PreToolUse', tool: 'Bash', command: 'ls', cwd: '/c' });
  assert.equal(p.tool_name, 'Bash');
  assert.equal(p.tool_input.command, 'ls');
  assert.equal(p.hook_event_name, 'PreToolUse');
});

test('try-hook: exit 2 blocks, other exits fail open, JSON decisions are read', () => {
  assert.equal(interpret({ status: 2, stdout: '', stderr: 'no' }, 'PreToolUse').decision, 'block');
  assert.equal(interpret({ status: 1, stdout: '', stderr: 'boom' }, 'PreToolUse').decision, 'error');
  const ask = JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: 'r' } });
  assert.equal(interpret({ status: 0, stdout: ask, stderr: '' }, 'PreToolUse').decision, 'ask');
  assert.equal(interpret({ status: 0, stdout: '{"decision":"block","reason":"r"}', stderr: '' }, 'Stop').decision, 'block');
  assert.equal(interpret({ status: 0, stdout: '', stderr: '' }, 'PreToolUse').decision, 'allow');
});

test('try-hook: plain stdout is context on SessionStart, invalid JSON is flagged', () => {
  assert.equal(interpret({ status: 0, stdout: 'hello', stderr: '' }, 'SessionStart').decision, 'context');
  const r = interpret({ status: 0, stdout: '{bad}', stderr: '' }, 'PreToolUse');
  assert.ok(r.notes.some((n) => /does not parse/.test(n)));
});

// convert-as-skill
const rule = (fm, body = '# Title\nBody line.\n') => `---\n${fm}\n---\n${body}`;

test('convert: an agent-requested rule keeps its body verbatim', () => {
  const body = '# API style\n\n- one\n- two  \n';
  const r = convertSource({ file: '/p/.cursor/rules/api-style.mdc', text: rule('description: "REST conventions"\nglobs:\nalwaysApply: false', body) });
  assert.equal(r.status, 'convert');
  assert.equal(r.name, 'api-style');
  assert.equal(r.skillMd, `---\nname: api-style\ndescription: "REST conventions"\n---\n${body}`);
});

test('convert: always-on, file-scoped and frontmatter-less rules are skipped unless asked', () => {
  const file = '/p/.cursor/rules/a.mdc';
  assert.equal(convertSource({ file, text: rule('description: "d"\nalwaysApply: true') }).status, 'skip');
  assert.equal(convertSource({ file, text: rule('description: "d"\nglobs: "**/*.ts"\nalwaysApply: false') }).status, 'skip');
  const kept = convertSource({ file, text: rule('description: "d"\nglobs: "**/*.ts"\nalwaysApply: false'), paths: true });
  assert.equal(kept.status, 'convert');
  assert.match(kept.skillMd, /paths: "\*\*\/\*\.ts"/);
  assert.equal(convertSource({ file, text: '# no frontmatter\n' }).status, 'skip');
});

test('convert: a command without frontmatter gets a drafted description and stays manual', () => {
  const text = '# Commit current work\nInstructions here.\n';
  const r = convertSource({ file: '/p/.cursor/commands/commit.md', text });
  assert.equal(r.status, 'convert');
  assert.equal(r.skillMd, `---\nname: commit\ndescription: "Commit current work"\ndisable-model-invocation: true\n---\n\n${text}`);
  assert.ok(r.warnings.some((w) => /inferred/.test(w)));
});

test('convert: command frontmatter keys are kept and nested folders are joined', () => {
  const text = '---\ndescription: "Write a note."\nargument-hint: "[topic]"\n---\nDo it: $ARGUMENTS\n';
  const r = convertSource({ file: '/p/.claude/commands/notes/write.md', text });
  assert.equal(r.name, 'notes-write');
  assert.match(r.skillMd, /argument-hint: "\[topic\]"/);
  assert.match(r.skillMd, /disable-model-invocation: true/);
  assert.ok(r.skillMd.endsWith('Do it: $ARGUMENTS\n'));
  assert.ok(r.warnings.some((w) => /nested/.test(w)));
});

test('convert: a subagent drops tools with a warning; --fork adds context: fork', () => {
  const text = '---\nname: summarizer\ndescription: "Summarizes. Use after a big read."\ntools: Read\nmodel: haiku\n---\nRead and summarize.\n';
  const plain = convertSource({ file: '/p/agents/summarizer.md', text });
  assert.equal(plain.status, 'convert');
  assert.match(plain.skillMd, /model: haiku/);
  assert.doesNotMatch(plain.skillMd, /tools:/);
  assert.ok(plain.warnings.some((w) => /dropped agent-only key\(s\): tools/.test(w)));
  assert.match(convertSource({ file: '/p/agents/summarizer.md', text, fork: true }).skillMd, /context: fork/);
});

test('convert: errors for unknown kind, bad names and missing descriptions', () => {
  assert.equal(convertSource({ file: '/p/notes.md', text: 'x' }).status, 'error');
  assert.equal(convertSource({ file: '/p/.cursor/rules/a.mdc', text: rule('alwaysApply: false'), name: 'Bad_Name' }).status, 'error');
  assert.equal(convertSource({ file: '/p/agents/a.md', text: '---\nname: a\n---\nbody\n' }).status, 'error');
  assert.equal(slugify('My Rule.mdc'), 'my-rule');
});

// super-verify read-run
import { parseSummary, verdict } from '../skills/engineering/super-verify/scripts/read-run.mjs';

const judge = (text, exit, runner) => verdict({ exit, summary: parseSummary(text, runner) });

test('read-run: a run that executed nothing is inconclusive, not a pass', () => {
  assert.equal(judge('============ no tests ran in 0.01s ============', 0).verdict, 'inconclusive');
  assert.equal(judge('0 tests, 0 failures', 0).verdict, 'inconclusive');
  assert.equal(judge('running 0 tests\ntest result: ok. 0 passed; 0 failed; 0 ignored', 0).verdict, 'inconclusive');
  assert.equal(judge('No tests executed!', 0).verdict, 'inconclusive');
});

test('read-run: counts per runner and fails on failures or a non-zero exit', () => {
  assert.equal(judge('3 passed, 1 skipped in 0.2s', 0).verdict, 'pass');
  assert.equal(judge('1 failed, 2 passed in 0.2s', 1).verdict, 'fail');
  assert.equal(judge('Tests:       1 failed, 2 passed, 3 total', 1).verdict, 'fail');
  assert.equal(judge('Tests  2 passed (2)', 0).verdict, 'pass');
  assert.equal(judge('42 tests, 0 failures, 3 skipped', 0).verdict, 'pass');
  assert.equal(parseSummary('42 tests, 0 failures, 3 skipped').passed, 39);
  assert.equal(judge('test result: ok. 5 passed; 0 failed; 1 ignored\ntest result: ok. 2 passed; 0 failed; 0 ignored', 0).verdict, 'pass');
  assert.equal(parseSummary('test result: ok. 5 passed; 0 failed; 1 ignored\ntest result: ok. 2 passed; 0 failed; 0 ignored').passed, 7);
  assert.equal(judge('OK (12 tests, 30 assertions)', 0).verdict, 'pass');
  assert.equal(judge('4 examples, 1 failure', 1).verdict, 'fail');
  assert.equal(judge('ℹ tests 13\nℹ pass 13\nℹ fail 0\nℹ cancelled 0\nℹ skipped 0\nℹ todo 0', 0).verdict, 'pass');
  assert.equal(judge('--- PASS: TestA (0.00s)\n--- FAIL: TestB (0.00s)', 1).verdict, 'fail');
});

test('read-run: all-skipped, unknown output and a missing exit code are not passes', () => {
  assert.equal(judge('0 passed, 4 skipped in 0.1s', 0, 'pytest').verdict, 'inconclusive');
  assert.equal(judge('hello', 0).verdict, 'inconclusive');
  assert.equal(judge('hello', 1).verdict, 'fail');
  assert.equal(judge('3 passed in 0.1s', undefined).verdict, 'inconclusive');
  assert.equal(judge('3 passed in 0.1s', 1).verdict, 'fail');
});
