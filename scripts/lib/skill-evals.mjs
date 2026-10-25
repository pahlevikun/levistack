import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { scanTree } from './tree.mjs';

/** @typedef {{ id?: number, prompt: string, expected_output: string, assertions: string[], files?: string[] }} EvalRow */
/** @typedef {{ skill_name: string, evals: EvalRow[] }} EvalsFile */
/** @typedef {{ request: string, must: string[], owner?: string, guide?: string }} CaseRow */
/** @typedef {{ cases: CaseRow[] }} CasesFile */

export function catalogSkills(root) {
  const tree = scanTree(root);
  const out = [];
  for (const g of tree.groups) {
    for (const s of g.skills) {
      out.push({ group: g.name, name: s.name, description: s.fm.description ?? '' });
    }
  }
  return out.sort((a, b) => `${a.group}/${a.name}`.localeCompare(`${b.group}/${b.name}`));
}

export function evalsDir(root, group, name) {
  return join(root, 'skills', group, name, 'evals');
}

export function readEvalFixture(root, group, name) {
  const dir = evalsDir(root, group, name);
  const evalsPath = join(dir, 'evals.json');
  const casesPath = join(dir, 'cases.json');
  if (existsSync(evalsPath)) {
    const data = JSON.parse(readFileSync(evalsPath, 'utf8'));
    return { kind: 'evals', path: evalsPath, data };
  }
  if (existsSync(casesPath)) {
    const data = JSON.parse(readFileSync(casesPath, 'utf8'));
    return { kind: 'cases', path: casesPath, data };
  }
  return null;
}

/**
 * @param {string} root
 * @param {{ strict?: boolean }} [opts]
 * @returns {string[]}
 */
export function validateSkillEvalFixtures(root, { strict = false } = {}) {
  const errors = [];
  for (const { group, name } of catalogSkills(root)) {
    const id = `skill ${group}/${name}`;
    const fixture = readEvalFixture(root, group, name);
    if (!fixture) {
      errors.push(`${id}: missing evals/evals.json or evals/cases.json`);
      continue;
    }
    if (fixture.kind === 'evals') {
      const file = fixture.data;
      if (file.skill_name !== name) {
        errors.push(`${id}: evals.json skill_name "${file.skill_name}" must equal "${name}"`);
      }
      if (!Array.isArray(file.evals) || file.evals.length < 1) {
        errors.push(`${id}: evals.json needs a non-empty evals array`);
      } else {
        for (const row of file.evals) {
          if (!row.prompt || !row.expected_output) {
            errors.push(`${id}: each eval needs prompt and expected_output`);
            break;
          }
          if (!Array.isArray(row.assertions) || row.assertions.length < 1) {
            errors.push(`${id}: each eval needs at least one assertion`);
            break;
          }
        }
      }
    } else {
      const file = fixture.data;
      if (!Array.isArray(file.cases) || file.cases.length < 1) {
        errors.push(`${id}: cases.json needs a non-empty cases array`);
      } else {
        for (const row of file.cases) {
          if (!row.request || !Array.isArray(row.must) || row.must.length < 1) {
            errors.push(`${id}: each case needs request and a non-empty must list`);
            break;
          }
        }
      }
    }
  }
  if (strict) {
    for (const { group, name } of catalogSkills(root)) {
      const dir = evalsDir(root, group, name);
      for (const extra of ['evals.json', 'cases.json']) {
        const p = join(dir, extra);
        if (existsSync(p) && !readEvalFixture(root, group, name)) {
          errors.push(`skill ${group}/${name}: unreadable eval fixture`);
        }
      }
    }
  }
  return errors;
}
