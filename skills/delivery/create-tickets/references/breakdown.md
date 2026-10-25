# Break work into tickets

Use this when the source is bigger than one story. It gives you a list of thin tickets, each with the tickets that block it, and checks the list with the user before any full body is written. The slicing rules live in `write-plan` (`references/slicing.md`). This file is the ticket side of them.

## Contents
- Steps
- The cut
- The quiz
- The exception
- Do not

## Steps

1. **Start from slices.** If a sliced plan exists, use it: one ticket per slice, and carry each slice's **Blocked by** over. If there is only a big source (a spec, a doc, a chat), cut it into slices first using the rules below.
2. **Draft the list,** not the bodies. One line per ticket: number, title, what it delivers, blocked by.
3. **Quiz the user** on the list (below). Change it until they agree.
4. **Write the bodies** with the story template, only for the agreed tickets.
5. **Publish** in dependency order, blockers first (see Route B in `SKILL.md`).

## The cut

- **End to end.** A ticket reaches every layer it needs (data, API, screen, tests), so it can be shown or checked alone. Do not make one ticket per layer.
- **Small.** One person or one fresh agent session can finish it.
- **Real blockers only.** A ticket waits on another only when data flows from it, a contract must exist first, or a shared piece is missing. Never add order to look tidy.
- **Ready tickets.** A ticket that waits on nothing can start now. Say which ones those are.
- **Make room first.** If the code must be reshaped before the feature fits, that is ticket 1, with no behavior change.
- **Project words.** Titles use the repo's glossary.

## The quiz

Show the numbered list. Then ask one question at a time, each with your recommendation, and wait for the answer:

1. Is the size right? Are any tickets too big, or too small to stand alone?
2. Is each "blocked by" real, or does a ticket wait on something that does not gate it?
3. Should any tickets be merged or split?
4. Is any ticket a layer in disguise ("build the API") instead of something a user can see?

Do not publish and do not write full bodies until the user says the list is right.

## The exception

A sweeping mechanical change (a rename, a type change across the whole codebase) breaks the build until it is finished, so a split by feature will not compile. Make it one ticket. Or make three: build the tool that does the change, run it once, and check with the compiler.

## Do not

- Publish before the quiz is answered.
- Change or close the parent issue the tickets came from.
- Invent a blocker the source does not have.
- Put file paths in a ticket. They go stale.
