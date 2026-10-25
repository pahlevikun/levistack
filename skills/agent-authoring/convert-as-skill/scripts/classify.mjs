#!/usr/bin/env node
// Pick exactly one convert-as-skill use case (or ask / reject). Run before opening a GUIDE.
//
//   node classify.mjs [--text "<user request>"] [--json] [path...]
//
// File layout beats wording. Merge wording beats "convert" when two-plus skill
// folders are present. Never default to conversation.
import { existsSync, readdirSync, statSync } from 'node:fs';
import { basename, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const DOCUMENT_EXTS = new Set([
  '.pdf', '.epub', '.docx', '.html', '.htm', '.xhtml', '.rtf',
  '.mobi', '.azw', '.azw3', '.txt', '.text', '.rst', '.adoc', '.asciidoc',
]);

export const GUIDES = {
  'from-rule': 'specialities/from-rule/GUIDE.md',
  'from-command': 'specialities/from-rule/GUIDE.md',
  'from-agent': 'specialities/from-agent/GUIDE.md',
  'from-conversation': 'specialities/from-conversation/GUIDE.md',
  'from-document': 'specialities/from-document/GUIDE.md',
  'merge-skills': 'specialities/merge-skills/GUIDE.md',
};

const DOCS_DIRS = new Set(['docs', 'documentation', 'doc', 'handbook', 'manuals', 'papers']);
const KIND_ORDER = ['merge-skills', 'from-agent', 'from-command', 'from-rule', 'from-document', 'from-conversation'];

const SCRATCH = /\b(from scratch|new skill|write a skill|create a skill|add a skill)\b/i;
const NEW_RULE = /\b(new rule|create a rule|write a rule|add a rule)\b/i;
const NEW_COMMAND = /\b(new command|create a command|write a (slash )?command|add a command)\b/i;
const NEW_AGENT = /\b(new (sub)?agent|create (an |a )?(sub)?agent|write (an |a )?(sub)?agent|add (an |a )?(sub)?agent)\b/i;
const MERGE = /\b(merge|combine|into one skill)\b/i;
const CONVO = /\b(conversation|this (chat|session)|prior session|previous session|last (time|session)|what we just did|save this session|harvest|transcript)\b/i;

export function inspectPath(file, fs = { existsSync, statSync, readdirSync }) {
  const parts = (file.startsWith('http://') || file.startsWith('https://') ? [file] : resolve(file).split(sep)).map((p) => p.toLowerCase());
  const ext = extname(file).toLowerCase();
  const name = basename(file);
  const info = { path: file, exists: false, isDirectory: false, isFile: false, hasSkillMd: false, ext, parts, name };
  if (/^https?:\/\//i.test(file)) return info;
  try {
    if (!fs.existsSync(file)) return info;
    info.exists = true;
    const st = fs.statSync(file);
    info.isDirectory = st.isDirectory();
    info.isFile = st.isFile();
    if (info.isDirectory) {
      info.hasSkillMd = fs.existsSync(`${file.replace(/[/\\]+$/, '')}${sep}SKILL.md`)
        || (typeof fs.readdirSync === 'function' && fs.readdirSync(file).includes('SKILL.md'));
    } else if (name === 'SKILL.md') {
      info.hasSkillMd = true;
    }
  } catch {
    // Path is still classifiable from layout / extension.
  }
  return info;
}

export function kindFromInspect(info) {
  if (/^https?:\/\//i.test(info.path)) return 'from-document';
  if (info.hasSkillMd) return 'skill-dir';
  if (info.parts.includes('agents')) return 'from-agent';
  if (info.parts.includes('commands')) return 'from-command';
  if (info.parts.includes('rules') || info.ext === '.mdc') return 'from-rule';
  if (DOCUMENT_EXTS.has(info.ext)) return 'from-document';
  if (info.parts.some((p) => DOCS_DIRS.has(p))) return 'from-document';
  if (info.isDirectory && /^(docs?|documentation|handbook|manuals|papers)$/i.test(info.name)) return 'from-document';
  return 'unknown';
}

function urlsIn(text) {
  return [...(text.matchAll(/https?:\/\/[^\s)\]>'"]+/gi) ?? [])].map((m) => m[0]);
}

function job(kind, files, reason) {
  return { kind, files, reason, guide: GUIDES[kind] };
}

function ok(jobs) {
  return { status: 'ok', jobs };
}

function ask(question, jobs = []) {
  return { status: 'ask', jobs, question };
}

function reject(redirect, reason) {
  return { status: 'reject', jobs: [], redirect, reason };
}

export function classify({ paths = [], text = '', inspect = inspectPath } = {}) {
  const items = paths.map((p) => {
    const info = inspect(p);
    return { path: p, info, kind: kindFromInspect(info) };
  });
  const urls = urlsIn(text);
  if (!items.length && urls.length) {
    items.push(...urls.map((u) => ({ path: u, info: inspectPath(u), kind: 'from-document' })));
  }

  const byKind = new Map();
  for (const it of items) {
    if (it.kind === 'unknown') continue;
    if (!byKind.has(it.kind)) byKind.set(it.kind, []);
    byKind.get(it.kind).push(it.path);
  }
  const skillDirs = byKind.get('skill-dir') ?? [];
  const knownKinds = [...byKind.keys()].filter((k) => k !== 'skill-dir');
  const convertible = items.filter((it) => it.kind !== 'unknown');
  const mergeWords = MERGE.test(text);
  const convoWords = CONVO.test(text);

  if (skillDirs.length >= 2 && mergeWords && knownKinds.length === 0) {
    return ok([job('merge-skills', skillDirs, 'merge/combine wording with two or more skill folders')]);
  }
  if (skillDirs.length >= 2 && !mergeWords) {
    return ask('Merge these into one skill, or convert each separately?', [job('merge-skills', skillDirs, 'two skill folders without merge wording')]);
  }
  if (mergeWords && (skillDirs.length === 1 || knownKinds.length > 0)) {
    return ask('Merge needs two or more skill folders and no other kind in the same request. Drop the extra files, or convert them as separate jobs.');
  }
  if (mergeWords && skillDirs.length === 0 && items.length === 0) {
    return ask('Which skill folders should be merged? Each must contain SKILL.md.');
  }
  if (skillDirs.length === 1 && knownKinds.length === 0 && !convoWords) {
    return ask('That path is already a skill. Merge it with another skill, or edit it with create-skill.');
  }
  if (skillDirs.length && knownKinds.length) {
    return ask('A skill folder plus another kind is mixed. Merge skills, or convert the other files, as separate jobs.');
  }

  if (convertible.length && convoWords) {
    return ask('Files and a conversation were both named. Convert the files, harvest the conversation, or say which one this request is.');
  }

  if (knownKinds.length >= 1) {
    const jobs = KIND_ORDER.filter((k) => byKind.has(k)).map((k) =>
      job(k, byKind.get(k), `path layout: ${k}`),
    );
    return ok(jobs);
  }

  if (items.length && convertible.length === 0) {
    return ask('Cannot tell the use case from those paths. Name a rule, command, agent, document, skill folder, or conversation.');
  }

  // No convertible files: wording only.
  if (SCRATCH.test(text) && !NEW_RULE.test(text) && !NEW_COMMAND.test(text) && !NEW_AGENT.test(text)) {
    return reject('create-skill', 'from scratch / new skill with no source file');
  }
  if (NEW_RULE.test(text)) return reject('create-rule', 'new rule with no file to convert');
  if (NEW_COMMAND.test(text)) return reject('create-command', 'new command with no file to convert');
  if (NEW_AGENT.test(text)) return reject('create-agent', 'new agent with no file to convert');
  if (convoWords) {
    return ok([job('from-conversation', [], 'conversation/session wording and no convertible files')]);
  }
  return ask('Convert a rule, command, agent, document, conversation, or merge existing skills? Attach the source or say which.');
}

function parseArgs(argv) {
  const paths = [];
  let text = '';
  let json = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') json = true;
    else if (a === '--text') {
      if (argv[i + 1] === undefined) throw new Error('--text needs a value');
      text = argv[++i];
    } else if (a.startsWith('--')) {
      throw new Error(`unknown flag ${a}`);
    } else paths.push(a);
  }
  return { paths, text, json };
}

function format(result) {
  if (result.status === 'ok') {
    const lines = result.jobs.map((j) => `ok ${j.kind} (${j.files.join(', ') || 'no files'})\n  ${j.reason}\n  load ${j.guide}`);
    return lines.join('\n');
  }
  if (result.status === 'ask') {
    return `ask ${result.question}`;
  }
  return `reject → ${result.redirect}\n  ${result.reason}`;
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`classify: ${e.message}`);
    process.exit(2);
  }
  const result = classify(parsed);
  if (parsed.json) console.log(JSON.stringify(result, null, 2));
  else console.log(format(result));
  if (result.status !== 'ok') process.exit(result.status === 'ask' ? 3 : 4);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
