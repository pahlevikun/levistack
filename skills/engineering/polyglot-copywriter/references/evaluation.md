# Skill evaluation

Use this when you change core rules, the language router, or Polyglot Voice modes. Do not score the skill by whether a regional mascot word appeared.

## What “working” means

1. Facts and technical actions stay the same when only style changes
2. Protected artifacts that are not the task target stay identical
3. Style feels possible for a speaker who knows that variety — or the fallback is honest
4. Register, intensity, speech level, poetic style, pronouns, and user bans are kept
5. Profiles do not collapse into stereotype or a random regional mix
6. Safety and permission stay intact
7. English output stays on the Indo-US plain bar (simple words, one intention per sentence)
8. **Every language** stays on the [simple-prose.md](simple-prose.md) bar — common words, short active sentences; formal register ≠ complicated grammar

## Scenario matrix

Test each high-traffic language (`english`, `indonesia`, plus any language you changed) at least on:

| Scenario | Must stay | Style risk |
|---|---|---|
| Explain a bug | cause, location, symbol, certainty | slang hides the diagnosis |
| Report a change | file, line, test, result | success claim drifts |
| Ask for clarification | the decision needed | pronouns too close |
| Code review | severity and impact | local tone becomes dismissive |
| Destructive warning | target, effect, need for OK | warning sounds unserious |
| Email / letter / announcement | intention in sentence 1 | warmup and fancy words |
| Security refusal | limit and safe alternative | style weakens the no |

Also test identifier edits that **are** the task target. The skill fails if language rules freeze those. Only untargeted references must stay identical.

## Automatic invariants

The harness checks:

- listed `preserve` substrings appear unchanged
- listed `require` substrings appear
- `first_paragraph_require` appears in the first paragraph
- `forbid_patterns` do not match (`iu`)
- `human_review` is recorded for a person to judge naturalness

Do not write tests that only require `rek`, `mah`, `gue`, or `lo` to appear. That pushes caricature.

## Run the harness

From the skill folder:

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate_output.py <case-id> <output-file>
```

[evals/cases.json](../evals/cases.json) stores prompts, preserve/require/forbid lists, and human-review notes. Automatic checks do not demand a full gold answer. Add a case when a new invariant fails; do not add a fixture for one lucky wording.

## Self-check rubric (before delivery)

Agents run this mentally on important drafts; users only see scores when they asked to score.

| Axis | What to check | Weight |
|---|---|---|
| **AI-smell** | Cluster density per [noslop-prose.md](noslop-prose.md) — not isolated tells; em-dash density counts | 25% |
| **Calque / translationese** | Sounds translated or stiff for target language; see [techniques/natural-writing.md](techniques/natural-writing.md) | 20% |
| **Register match** | Fits `baku` / `profesional` / `santai` + channel + use case | 20% |
| **Clarity** | Sentence 1 job; facts scannable; no buried lead; [simple-prose.md](simple-prose.md) bar | 20% |
| **Dialect honesty** | Overlay used correctly; no fake regional soup; umbrella limits stated | 15% |

**Informal bands:** 85+ ship with spot-check; 70–84 one more pass on worst axis; below 70 rework lead and thin clusters.

**Humanize / rewrite tasks:** also run [techniques/humanize-workflow.md](techniques/humanize-workflow.md) verify step (read aloud; portability test; no invented facts; survivor tells; rewrite self-check).

**Review / development tasks:** when paragraphs read list-like, also apply [techniques/flow-by-relation.md](techniques/flow-by-relation.md).

**Marketing tasks:** also check [techniques/marketing-copy.md](techniques/marketing-copy.md) checklist (one primary CTA, proof from user only).

### Graded dimensions (human review helper)

For high-stakes rewrite or review evals, reviewers may score optional axes on 1–5 (documentation only — not a CI gate):

| Dimension | Question |
|---|---|
| **Specificity** | Does the output name actors, mechanisms, limits, or carriers? |
| **Relation-clarity** | Are hinges and contrasts earned, not decorative? |
| **Evidence fit** | Do claims stay within source attribution and scope? |
| **Restraint** | Did the agent avoid over-editing earned patterns? |

Record scores in manual eval notes; do not block `validate_skill.py` on them.

## Simple prose self-check (before delivery)

Run with [simple-prose.md](simple-prose.md) on any user-facing draft:

- [ ] Could a tired teammate parse this in one read without re-scanning for the point?
- [ ] Is any word replaceable with a shorter common synonym in the target language?
- [ ] Does each explanatory sentence carry one main idea (split overloaded lines)?
- [ ] Any nested clause, passive stack, or jargon verb that exists only to sound "professional"? Replace or split.

## Humanizer self-check (before delivery)

Run on any rewrite, humanize or review task, with [humanizer-patterns.md](humanizer-patterns.md):

- [ ] Strongest tells (§1 to §5, §13, §22, §23) are gone or kept on purpose (earned contrast, real triad).
- [ ] The five survivors are clear: §1 contrast, §2 closer, §6 triad, §8 dash, §19 bold label.
- [ ] No added or dropped fact, name, number, date, quote, citation or ranking.
- [ ] No chatbot wrapper (§22). No guess dressed as fact (§23).
- [ ] In a reply, the decision comes first (§26).
- [ ] The rewrite is simpler than the source, not fancier ([simple-prose.md](simple-prose.md)).
- [ ] File mode: only prose changed. Embedded mode: only the final text returned.
- [ ] It still sounds like a person: voice sample matched, one specific detail or honest uncertainty kept.

## Dash and semicolon self-check (before delivery)

Run on chat, email, incident, and humanize drafts:

- [ ] Scan for `—`, `–`, and `;`. First principle: none in final prose ([humanizer-patterns.md](humanizer-patterns.md) §8). Allowed only for `baku`, a user sample that uses them, or quoted text, and then at most one per ~200 words. Split with comma, period, colon or parentheses.
- [ ] No `fact — explanation — conclusion` chains; each idea gets its own sentence when possible.

## Mode and fidelity check (before delivery)

- [ ] Requested mode was performed (interview did not draft first; review did not rewrite).
- [ ] No fact, attribution, scope, condition, quote, link, or experience drifted.
- [ ] Hollow authored prose either has real source material or says so / uses `[TK:]`.
- [ ] Voice sample and fingerprint changed style only.
- [ ] Medium still works (procedures scan, emails state the ask, incidents keep impact).

## Suggested release gate

- No change to untargeted protected artifacts
- No lost fact, permission, or warning
- No markers from another profile without a mix request
- Pronoun, speech-level, intensity, and prose-style overrides are kept
- Umbrella and limited packs handled per `pack.md`; unknown names not invented
- SKILL.md still routes to the required reference files
- `python3 scripts/validate_skill.py` passes with all registry rows validated
