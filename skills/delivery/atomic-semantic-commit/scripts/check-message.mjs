#!/usr/bin/env node
// Check commit messages against the semantic format and the STE rules in references/.
//
//   node check-message.mjs "<message>" ...
//   node check-message.mjs --file .git/COMMIT_EDITMSG      (also works as a commit-msg hook: ... --file "$1")
//   node check-message.mjs --range HEAD~5..HEAD            (check existing commits)
//   echo "<message>" | node check-message.mjs --stdin
//
// Options: --types=base   only the seven semantic types (otherwise perf, build, ci, revert are allowed)
//          --strict       warnings also fail
//          --json         machine-readable output
// Exit code 1 when a message has an error (or a warning with --strict).
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const BASE_TYPES = ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'];
export const EXTRA_TYPES = ['perf', 'build', 'ci', 'revert'];
export const SUBJECT_AIM = 50;
export const SUBJECT_MAX = 72;
export const BODY_WRAP = 72;
export const SENTENCE_MAX = 20;

const NOT_IMPERATIVE = /^(added|fixed|removed|updated|changed|renamed|moved|replaced|created|deleted|improved|implemented|refactored|extracted|adds|fixes|removes|updates|changes|renames|moves|replaces|creates|deletes|improves|adding|fixing|removing|updating|changing|renaming|moving|replacing|creating|deleting|improving|implementing)\b/i;
const VAGUE = /\b(various|several|some stuff|stuff|things|misc|miscellaneous|etc|wip|tweaks?|minor changes?|small (fix|fixes|changes?)|improvements?|enhancements?)\b/i;
const SECOND_ACTION = /\band\s+(add|fix|remove|rename|move|replace|extract|change|use|delete|create|bump|drop|handle|enable|disable|run|write|merge|split|update|refactor|set|make)\b/i;
const FIRST_PERSON = /^(this commit|i |we |now |currently |as requested)/i;
const ATTRIBUTION = /generated with|co-authored-by:|assisted-by:|signed-off-by:/i;
const AUTO = /^(merge |revert "|fixup! |squash! |amend! )/i;

const stripCode = (s) => s.replace(/`[^`]*`/g, '');

export function checkMessage(raw, opts = {}) {
  const findings = [];
  const add = (severity, code, message, line = 1) => findings.push({ severity, code, line, message });
  const lines = raw
    .replace(/\r\n/g, '\n')
    .split('\n')
    .filter((l) => !l.startsWith('#'));
  while (lines.length && lines[lines.length - 1].trim() === '') lines.pop();
  if (!lines.length || lines[0].trim() === '') {
    add('error', 'empty', 'the message is empty or starts with a blank line');
    return findings;
  }
  const subject = lines[0];
  if (AUTO.test(subject)) {
    add('info', 'auto-message', 'merge, revert, fixup and squash messages are not checked');
    return findings;
  }

  const m = subject.match(/^([A-Za-z]+)(?:\(([^)]*)\))?(!)?: (.+)$/);
  if (!m) {
    add('error', 'format', 'use "<type>(<scope>): <subject>", for example "fix(auth): retry token refresh"');
  } else {
    const [, type, scope, bang, text] = m;
    const all = opts.baseOnly ? BASE_TYPES : [...BASE_TYPES, ...EXTRA_TYPES];
    if (type !== type.toLowerCase()) add('error', 'type-case', `type "${type}" must be lowercase`);
    else if (!all.includes(type)) add('error', 'type', `unknown type "${type}". Use: ${all.join(', ')}`);
    else if (EXTRA_TYPES.includes(type)) add('info', 'extra-type', `"${type}" is outside the seven base types. Use it only if the repository already does`);
    if (scope !== undefined) {
      if (scope.trim() === '') add('error', 'scope-empty', 'the scope is empty. Remove the parentheses or name the context');
      else if (/[A-Z\s]/.test(scope)) add('warn', 'scope-format', `scope "${scope}" should be one lowercase word`);
    }
    if (NOT_IMPERATIVE.test(text)) add('warn', 'mood', 'use the imperative, present tense: "add", "fix", "remove". Not "added", "adds", "adding"');
    if (/^[A-Z][a-z]+$/.test(text.split(/\s+/)[0])) add('warn', 'case', 'start the subject in lowercase, unless the repository does otherwise');
    if (VAGUE.test(text)) add('warn', 'vague', `vague word "${text.match(VAGUE)[0]}". Say what changed`);
    if (SECOND_ACTION.test(text)) add('warn', 'two-actions', 'the subject names a second action after "and". Split the commit');
    if (/[—–;]/.test(text)) add('warn', 'punctuation', 'no em dash, en dash or semicolon. Use a period or a colon');
    if (bang && !lines.slice(1).some((l) => l.trim())) add('warn', 'breaking-body', 'a breaking change needs a body that says what breaks and what to do');
    if (type === 'revert' && lines.length < 3) add('warn', 'revert-body', 'a revert needs a body that gives the reason');
  }
  if (subject.length > SUBJECT_MAX) add('error', 'subject-length', `the subject is ${subject.length} characters. The hard limit is ${SUBJECT_MAX}`);
  else if (subject.length > SUBJECT_AIM) add('warn', 'subject-long', `the subject is ${subject.length} characters. Aim for ${SUBJECT_AIM}`);
  if (/[.]$/.test(subject)) add('error', 'subject-period', 'no period at the end of the subject');

  if (lines.length > 1 && lines[1].trim() !== '') add('error', 'blank-line', 'leave one blank line after the subject', 2);

  let inFence = false;
  lines.slice(2).forEach((l, idx) => {
    const n = idx + 3;
    if (/^```/.test(l)) {
      inFence = !inFence;
      return;
    }
    if (inFence || /^ {4}|^\t/.test(l) || l.trim() === '') return;
    const trailer = /^[A-Za-z-]+: /.test(l) && !/\s{2}/.test(l) && /^(BREAKING CHANGE|Closes|Fixes|Refs|Co-authored-by|Signed-off-by|Assisted-by|Reviewed-by|Related)/i.test(l);
    if (ATTRIBUTION.test(l)) add('warn', 'attribution', 'AI or co-author attribution. Omit it unless the user rule requires a trailer', n);
    if (trailer || /^https?:\/\//.test(l.trim())) return;
    if (l.length > BODY_WRAP && !/https?:\/\//.test(l)) add('warn', 'wrap', `line is ${l.length} characters. Wrap at ${BODY_WRAP}`, n);
    const prose = stripCode(l);
    if (/[—–;]/.test(prose)) add('warn', 'punctuation', 'no em dash, en dash or semicolon in prose. Use a period or a colon', n);
    const text = prose.replace(/^\s*[-*]\s+/, '');
    if (FIRST_PERSON.test(text)) add('warn', 'voice', 'do not write "this commit", "I", "we", "now" or "currently". The diff shows what changed', n);
    for (const sentence of text.split(/(?<=[.!?])\s+/)) {
      const words = sentence.trim().split(/\s+/).filter(Boolean).length;
      if (words > SENTENCE_MAX) add('warn', 'sentence-length', `sentence has ${words} words. Use ${SENTENCE_MAX} or fewer`, n);
    }
  });
  if (subject.length > 0 && ATTRIBUTION.test(subject)) add('warn', 'attribution', 'attribution text in the subject', 1);
  return findings;
}

function splitLogOutput(out) {
  return out.split('\u0000').map((s) => s.replace(/^\n+/, '')).filter((s) => s.trim());
}

function parseArgs(argv) {
  const o = { messages: [], files: [], range: null, stdin: false, json: false, strict: false, baseOnly: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') o.json = true;
    else if (a === '--strict') o.strict = true;
    else if (a === '--stdin') o.stdin = true;
    else if (a === '--types=base') o.baseOnly = true;
    else if (a === '--file') o.files.push(argv[++i]);
    else if (a === '--range') o.range = argv[++i];
    else if (!a.startsWith('--')) o.messages.push(a);
  }
  return o;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const o = parseArgs(process.argv.slice(2));
  const items = o.messages.map((m) => ({ label: m.split('\n')[0], text: m }));
  for (const f of o.files) items.push({ label: f, text: readFileSync(f, 'utf8') });
  if (o.stdin) items.push({ label: 'stdin', text: readFileSync(0, 'utf8') });
  if (o.range) {
    const out = execFileSync('git', ['log', '--format=%h %s%n%b%x00', o.range], { encoding: 'utf8' });
    for (const chunk of splitLogOutput(out)) {
      const [first, ...rest] = chunk.split('\n');
      const sp = first.indexOf(' ');
      items.push({ label: first.slice(0, sp), text: `${first.slice(sp + 1)}\n${rest.length && rest.join('\n').trim() ? `\n${rest.join('\n')}` : ''}` });
    }
  }
  if (!items.length) {
    console.error('usage: node check-message.mjs "<message>" | --file <path> | --range <a..b> | --stdin [--types=base] [--strict] [--json]');
    process.exit(2);
  }
  const results = items.map((it) => ({ label: it.label, findings: checkMessage(it.text, { baseOnly: o.baseOnly }) }));
  const failing = results.some((r) => r.findings.some((f) => f.severity === 'error' || (o.strict && f.severity === 'warn')));
  if (o.json) console.log(JSON.stringify(results, null, 2));
  else {
    for (const r of results) {
      const real = r.findings.filter((f) => f.severity !== 'info');
      console.log(`${real.length ? (real.some((f) => f.severity === 'error') ? 'FAIL' : 'WARN') : 'OK  '} ${r.label}`);
      for (const f of r.findings) console.log(`     ${f.severity.toUpperCase().padEnd(5)} ${f.code.padEnd(15)} line ${f.line}: ${f.message}`);
    }
  }
  if (failing) process.exitCode = 1;
}
