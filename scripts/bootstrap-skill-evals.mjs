#!/usr/bin/env node
/**
 * Create evals/evals.json for catalog skills that lack evals/evals.json or evals/cases.json.
 * Idempotent: skips skills that already have a fixture.
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { catalogSkills, evalsDir, readEvalFixture } from './lib/skill-evals.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function useWhenSnippet(description) {
  const m = description.match(/Use when ([^.]+(?:\.[^N]|[^.])*)/);
  if (m) return m[1].trim().slice(0, 220);
  return 'the task described in the skill description';
}

function notForSnippet(description) {
  const m = description.match(/Not for ([^.]+)/);
  return m ? m[1].trim() : null;
}

function primaryPrompt(name, description) {
  const when = useWhenSnippet(description);
  return `Use the ${name} skill for a typical request that matches: ${when}. Follow SKILL.md and return the skill's normal deliverable shape.`;
}

function boundaryPrompt(name, description) {
  const nf = notForSnippet(description);
  if (nf) {
    return {
      prompt: `Handle a request that clearly belongs to ${nf}, not ${name}. The user did not ask for ${name}.`,
      expected_output: `Does not run ${name} as the primary workflow. Routes to the neighbor named in Not for or asks one clarifying question.`,
      assertions: [`Recognizes the Not for boundary`, `Does not apply ${name} procedures to the wrong job`],
    };
  }
  return {
    prompt: `Say hello and ask what I should work on next. Do not invent a ${name} task.`,
    expected_output: `Does not force ${name} without a matching user request.`,
    assertions: ['Does not invoke skill workflow without a trigger', 'Stays conversational or asks what is needed'],
  };
}

function buildEvals(name, description) {
  const boundary = boundaryPrompt(name, description);
  return {
    skill_name: name,
    evals: [
      {
        id: 1,
        prompt: primaryPrompt(name, description),
        expected_output: `Uses ${name} per SKILL.md modes and boundaries. Delivers the documented output without skipping verification steps the skill requires.`,
        assertions: [
          `Uses ${name} workflow`,
          'Honors read-only or approval rules from the skill',
          'Names checks run or gaps when a gate could not run',
        ],
        files: [],
      },
      {
        id: 2,
        prompt: boundary.prompt,
        expected_output: boundary.expected_output,
        assertions: boundary.assertions,
        files: [],
      },
    ],
  };
}

let created = 0;
for (const { group, name, description } of catalogSkills(root)) {
  if (readEvalFixture(root, group, name)) continue;
  const dir = evalsDir(root, group, name);
  mkdirSync(dir, { recursive: true });
  const out = join(dir, 'evals.json');
  writeFileSync(out, `${JSON.stringify(buildEvals(name, description), null, 2)}\n`);
  created += 1;
  console.log(`wrote ${out}`);
}
console.log(`bootstrap-skill-evals: created ${created} fixture(s)`);
