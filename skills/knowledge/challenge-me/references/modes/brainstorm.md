# Mode: brainstorm

Ideas → a design the user agrees with **before** implementation. Tracks (not separate skills): new product vs existing product. Loop: `interview-loop.md`.

## When

User says brainstorm, ideate, think through this, design this before we code, new product, existing product feature.

## Tracks

Pick one; say it in a line.

| Track | Signal | Extra lenses |
|---|---|---|
| **New product** | Greenfield, 0→1, "what should we build" | Who is it for, why now, what "working" means, what you will not build |
| **Existing product** | Feature on a live system | Current behavior (look it up), who already depends on it, migration/compat, what not to break |

Other subjects (architecture sketch, UI concept, writing outline) stay on the matching domain stub after this mode.

## Do

1. **Do not implement.** No production patches, no "quick spike in the repo" unless they explicitly want a spike and you labeled it disposable.
2. Explore constraints: users, success, failure, time, non-goals. Numbered Q + rec + wait.
3. Put **at least four** approaches on the table when the shape is still open (the "past three" rule plus the obvious). Rec one.
4. Converge to a short shared design: problem, chosen approach, non-goals, open questions. Chat is enough; write `templates/decision-map.md` if they asked or the thread will span sessions.
5. If they then want an implementation-plan file → `write-plan`. Tickets → `create-tickets`. Target stack → `super-tech-blueprint`. Current-repo inventory → `codebase-learner`.

## Independent subsystems

If the idea is several products glued together, split them before anyone writes a plan. `write-plan` expects that split already happened.

## Do not

- Duplicate subagent orchestration from `do` / `make-plan`.
- Ship a novel-length spec nobody asked for.
- Treat "brainstorm" as permission to skip grilling hard decisions — switch to **grill** when the tree is the job.

## Triage first

Before you reply, ask: what do I know about what they want, and why?

- **The request already holds everything that matters** ("make the icon cornflower blue"). This is a quick, clear task. Do it, say what you did, and this mode is finished.
- **Something non-trivial is missing.** Start the conversation.

## Look first, then open

If there is an existing project, or the user gave you context (a spec, a plan, files, an earlier chat), read it before your first message. Keep reading until you can say how the relevant parts work today and what the change would touch. Never ask what that context already answers.

## The opening message

Pick the one that fits.

- **They already said what they want** (a spec, a plan, a detailed request). Write about 150 words. Say it back in your own words: what they want, who it is for, and why, as far as they said. Add what you found: how the relevant parts work today and what the change would touch. If you spotted something they may not have thought of (a conflict, a limit, a cheaper path), say it plainly. Leave how to build it for later. End with one line that invites corrections, then one question about what they want: the open point whose answer would change what gets built the most. Specs are often incomplete, so confirm before you build on one.
- **They have not.** Ask one open question about the biggest thing left unsettled, and say why you ask, meaning what the answer would change.

If the user did not ask for brainstorming by name, add one light line after your question: "Or if you would rather I just start, say so." If they take it, this mode is finished. Say any big how-it-is-made choice (platform, language, medium) in one plain line, then do the work through the normal flow.

## Questions

- **Open questions first.** Their own words carry intent that your options cannot. Offer a short menu only when they are stuck. When they say "just guess" or "what do you think?", propose something concrete. A proposal they can correct beats a question.
- **Build each question on their last answer** or on something you found, the way a sharp colleague would. Point at a consequence or a case they may have missed ("Voting closes before the meeting, and two members joined this month. Does someone who joins late get a vote?").
- **Say why you ask** when the reason is not plain.
- Use plain words, a little above where they are. Match their vocabulary.
- Once real options exist, the normal numbered question with a recommended answer applies again.

**Ground to cover.** This is territory, not a script. Do not read it out as questions.

- What kind of thing this is, and what makes it special.
- Why now, and what success looks like to them.
- Goals, non-goals and anti-goals.
- Prior art: what they have seen elsewhere, loved or hated.
- The current state: what exists, what they have tried.
- The details they care about.
- **How it gets made.** Find out early which choices (platform, language, tools, materials) they want to make, which they hand to you, and what they already have. Say your defaults in plain words, and record any choice you made as yours, never as something they agreed to.

**Offer recon.** Once you have some grounding and looking further would help, offer to look: deeper into their code or files, or the web. Say what you would look for. They decide.

## Approaches, play-back, brief

- Once you understand what they want, lay out the approaches in their own message: `references/core/approaches.md`.
- Alternate questions with short play-backs of what you understood: `references/core/play-back.md`.
- End with the written design, the fresh-reader check and the gate: `references/core/design-brief.md`. Template: `templates/design-brief.md`.

## Show, do not tell

Per question, ask: would they understand this better by seeing it? If yes, offer a sketch first, in its own message: a Mermaid diagram for flows and structure, or a throwaway page with a few look variants for a screen (see the prototype step in `product-polish-workflow`). Requirements, scope and trade-offs stay in text. A question about a screen is not automatically a visual question: "what kind of wizard do you want?" is a concept, and "which of these wizard layouts feels right?" is visual. If they decline, stay in text and do not offer again unless they bring it up.

## Spike to feel things out

A quick throwaway build is sometimes the cheapest way to learn what they want. Offer one when it would help. Label it throwaway. Keep tests minimal. Bring what you learned back into the conversation. Keeping a spike is a new request, and it goes back through the design gate.

## Red flags

| If you think | Remember |
|---|---|
| "I will give them a menu of what they might want." | Menus steer. Ask them to describe it first. |
| "I will fill the gaps with sensible defaults." | Fine, but say them out loud and mark them as yours. A default they never heard cannot be rejected. |
| "They answered my questions, so I will write the brief." | Lay out the approaches first, in their own message. |
| "They said it sounds good." | They approved what you showed. A brief you have not written is not approved. |
| "The spike works, so I will keep building on it." | Keeping it is a new request. Go back through the gate. |
| "I should explain the process first." | Ask your first question. The process shows itself. |

