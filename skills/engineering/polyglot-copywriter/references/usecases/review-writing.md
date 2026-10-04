# Review Writing

Covers: MR code review comments, 360 peer feedback, self-assessments.

---

## MR Code Review Comments

**Corpus**: 118 non-trivial review comments from one engineer, across several backend and workflow services.

### The 6 Core MR Review Rules

1. **"Can we...?" is the proposal vehicle** — never "you should". Suggestions are framed as team questions. (24 instances — the dominant pattern.)
2. **Close every proposal with a question** — `right?`, `ya?`, `wdyt?`. Never fully asserts even when clearly right.
3. **"we" not "you"** — 3.5× more likely. the author reviews as a teammate, not an evaluator above the author.
4. **Direct imperatives only for hygiene** — `please remove`, `please add changelog`, `please update`. Never imperative on architecture decisions.
5. **"I think" hedges opinions** — "I think we can remove this inline comment" vs. flat "remove this".
6. **"bang [name]" softens requests** — Indonesian honorific (`bang` = roughly "mate/bro for peer or older"). Makes direct asks feel collegial.

### Sample Comments (anonymized)

**Proposals with "can we":**
- `Can we use the workflow client here? if not exist I think we can create a new one`
- `can we define the error in errors.go? should be easier to test and read all error we have in this workflow`
- `bang can we add jitter here? I think we need to avoid thundering herd in the workflow service from burst hit`
- `I saw lot of raw query in this handler, can we create a repo layer instead? Seems we can leverage this as application layer feature instead of workflow layer.`
- `can we put timeout in each task?`

**Hygiene / nit delivery (only place for imperatives):**
- `bang minor ya, please remove the comment` (appears 4×)
- `bang [name], can we remove this inline doc? I feel this isn't really helpful`
- `personally this is AI slop, I think we are clear on this step without any inline comment`

**Confirmation-seeking tail "right?":**
- `This technically will never be reached, right? We are passing maxAttempts from config...`
- `if it's not found in the payload or throwing error, the expectation is it will use the default flow and namespace, right?`
- `@teammate if order.discount_flag is undefined, the condition become true, right? is it expected?`

**Security / architecture concern (longer comments):**
- `I suggest to keep the error response generic and just log failureReasons. If we expose failureReasons to the public, I don't think we'll pass the security sign-off.`
- `I'm still have doubts about the idempotency approach as we'll be relying on db connection pooling. Considering this service is accessed by many services, if the database connections run out, this app will go down.`

**Approval / agreement:**
- `agree pack 🫡`
- `Yes yes confirmed`
- `Just check it by myself, resolving this`
- `IMHO it's ok to not put error handler here. wdyt @person?` (approves but still asks)

### Long-Form Comment Structure (when needed)

All analytical comments follow:
1. **Observation** — what's in the code
2. **Concern / implication** — what could go wrong or what principle is at stake
3. **Suggested alternative** — prose ("I am thinking how if...") or code block
4. **Closing question** — `right?` / `ya?` / `wdyt?`

Closing question is almost never skipped.

### Nit Delivery

the author does NOT use `nit:` prefix. His nit pattern is:
- `bang minor ya, please remove the comment`
- `minor` + direct ask + `ya` softener

### "nit" Word Usage

The word "nit" appears **0 times** in 118 comments. "minor" appears 4 times, always inside the `bang minor ya` construct.

### Informal Markers (authentic — keep these)

- `eh btw,` — casual aside opener
- `bang [name]` — peer address (Indonesian honorific)
- `mas @name` — for senior teammates
- `ya` / `ya?` — Indonesian filler/softener in questions
- `iya` — Indonesian "yes" (`oh iya forgot that one bang`)
- `wdyt` — "what do you think?"
- `atleast` — consistent misspelling (appears 2×, keep as-is)
- `dont'` — casual inversion contraction
- 🫡 — approval emoji (one instance, approval context only)

### Review Comment Anti-Patterns
- ❌ "Great work on this! Just one small thing..." (filler praise before the point)
- ❌ "you should" or "you need to" (use "can we" instead)
- ❌ Asserting without a closing question on architectural decisions
- ❌ Comments without context ("This is wrong" — wrong how? what should it be?)
- ❌ Re-explaining the code back to the author
- ❌ "LGTM" on an MR with open threads

---

## 360 Peer Feedback

### Core Principles

1. **Behavior + Impact structure** — name the observable thing, then name the effect it had
2. **Specific over general** — "Sam's payments rollout coordination" > "Sam is great at coordination"
3. **Evidence-based** — must be tied to something that actually happened
4. **Warm but direct** — honest even when giving development feedback

### Structure Template

**Strengths:**
```
[Name] demonstrates [specific behavior] — for example, [concrete instance].
This [resulted in / enabled / contributed to] [specific impact].
```

**Development feedback:**
```
One area to grow: [specific pattern]. In [specific context], [what happened / what could go differently].
This would help [specific outcome for the team/project].
```

### Sampled Patterns (inferred from IDP + the author's team context)

Strength example:
> "Sam consistently picks up ownership on ambiguous cross-system issues — the auth service migration is a clear example. They didn't wait for a full spec, drove the technical direction, and unblocked the team. That kind of initiative changes the team's velocity."

Development example:
> "One thing I'd like to see more of: Alex taking a position early in design discussions. Often the right read is there, but it surfaces late. Earlier visibility on their perspective would improve decision speed."

### 70/20/10 Connection (for self-assessment)

When writing self-assessment, connect behaviors to IDP categories:
- Experience (70%): "On the checkout redesign, I drove X end-to-end..."
- Exposure (20%): "The legacy service deprecation discussion surfaced cross-domain exposure..."
- Education (10%): "The onboarding flow deep dive gave me context on..."

### Format Preferences

| Element | the author's approach |
|---|---|
| Length | 2–4 sentences per point — no paragraphs |
| Pronouns | Second person for feedback ("you", "your"), first for self-assessment ("I") |
| Tone | Peer-to-peer, not hierarchical — like a senior colleague, not an evaluator |
| Em dashes | Optional — can use for asides but don't overdo it |
| Grammar | Natural, complete English. Same Indo-US plain bar as email and letters. |

### Anti-Patterns for 360 Writing
- ❌ "John is a very dedicated and hardworking team member who always goes above and beyond"
  (adjective stacking + zero specificity)
- ❌ "I think John does a good job most of the time" (hedged to meaninglessness)
- ❌ Feedback that can't be traced to a specific event
- ❌ Starting with "I'd like to take this opportunity to..." 
- ❌ Ending with "I look forward to seeing continued growth" (empty closer)

---

## Self-Assessment Writing

### Structure

```
## What I focused on this review period
[1–2 sentences. IDP goal + sprint context.]

## What I delivered
[Bullets. Concrete. Specific MRs, numbers, outcomes.]

## Where I grew
[1–2 instances. Skill or domain expanded. Not just "I got better".]

## What's next
[1–2 next priorities. Framed as decisions I own, not wishes.]
```

### Voice Notes for Self-Assessment
- Own the work: "I drove", "I initiated", "I managed end-to-end"
- Acknowledge unglamorous work: "Not the most visible work but it cleared the path for..."
- Flag initiative: "No one asked me to — I identified this as the right next move"
- Be honest about effort: "This was a grind but the zero-rollback result validated the approach"
