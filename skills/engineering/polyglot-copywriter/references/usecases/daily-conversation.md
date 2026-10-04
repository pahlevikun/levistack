# Daily Conversation

Patterns drawn from a corpus of real chat messages.
Context: primarily CUI (Change User Information) project coordination.
Note: previous version was inferred from IDP docs — this version is from real messages.

---

Channel-wide FYI, blasts, and "tell the team" posts are **announcement** mode (`plain-comms.md` in this folder), not this file. This file is thread replies, DMs, standup, and huddle chat.

## Core Casual Principles

1. **No greeting in threads** — reply directly. Greetings only for new top-level messages or morning channel posts.
2. **Action commitment > permission-seeking** — "let me find the log" not "can I check the log?" He commits and goes.
3. **"mas"/"kak" is punctuation** — attached to almost every sentence with a name. Skipping it is the exception.
4. **Short messages, not long ones** — 60% are 50–200 chars. Long messages (200+) are reserved for MoMs and context-dumps for new joiners.
5. **Ends on a question when something is open** — ~23% of messages end with `?`. Otherwise just stops — no sign-off.
6. **Natural grammar even when short** — warmth comes from `mas`/`kak`/`ya`, not from missing verbs. "Seems BFF is not passing it in the header." New drafts do not copy old IDP agreement errors.

---

## Addressing People (mandatory pattern)

- **"mas @Name"** — default for male colleagues at peer level or senior. Used 43% of messages.
- **"kak @Name"** — for female colleagues (`kak @Francisca`)
- He almost never omits the honorific when making a request: "mas @X could you verify" not "@X could you verify"
- When tagging multiple people: "mas @X and mas @Y" or "mas @X kak @Y"

---

## Opening Patterns

**New top-level thread:**
- "Morning team, I'll WFH today & early out for..."
- "Hi team, @mentions — [action item or FYI]"
- "@Person — open question, are we going to use same template?"

**Thread reply:**
- Jumps straight in: "did you retry or is it your first attempt?"
- Contextualizing for a newcomer: "Ah for the context, right now we've completed [full paragraph]..."
- After a realization: "Ah I see" / "Ah ok mas so if I can summarize..."

**The `^` prefix (distinctive):**
- Points back to a previous message or adds attribution: `^sorry mas @Singgih please help ya on that, if needed let's have huddle`
- `^cc: @X @Y` — quiet notification line under someone else's message

---

## Hedge Words (use these, not others)

- **"seems"** — primary diagnostic hedge: "seems we need real otp?", "seems BFF not passing it in header", "seems sms and email still not using the same template"
- **"I think"** — for architectural opinions only: "I think we can be more patient", "I think we can apply that for both sms and whatsapp"
- **Parenthetical asides** for uncertainty: "(actually don't know where to create)" / "(apologize I mistakenly create)"
- **NOT "just", "honestly", "ngl", "tbh"** — these don't appear in Lark messages (they're IDP writing artifacts — wrong context)

---

## Follow-up / Escalation Pattern

Calm, soft, time-anchored:

1. First nudge: `Bumping on this mas @X and mas @Y`
2. Time-anchor: `btw mas, for production onboarding, can it be done by today's EOD? so I have time on tomorrow 1st half to check before Sanity`
3. Second follow-up: `mas, may I know if it's done?`
4. Re-ping with acknowledgment: `mas @Name sorry for mention you again, seems in production the SMS template still using...`

No "URGENT", no caps escalation. Uses EOD deadlines and time windows instead.
`"sorry for mention you again"` — acknowledges the imposition, doesn't belabor it, continues anyway.

---

## Technical Issue Explanation (informal)

Sequence: symptom → evidence → hypothesis

1. State the symptom: "Failing on FR due to issue on the model"
2. Attach evidence immediately: screenshot, log link, curl output
3. Hypothesis in parentheses: "seems BFF not passing it in header"

Never writes the full diagnosis upfront. Shows evidence, lets the reader see it.

---

## MoM / Summary Format

When writing meeting notes in Lark:

```
MoM from the call:

1. Topic
  a. Sub-point
  b. Sub-point

Action: [Person] will [verb] by [timeframe]
```

Closes with "We will target this by today" or a specific time commitment.

---

## Status Update Patterns

- "deployed kak @X"
- "now it's there mas inside example.com domain"
- "@X it's working fine mas, thankyou" + "shown as expected" (two one-liners, confirming same thing)
- "the team informed that FR is working, you can retry the flow"
- Never "Done." alone — always attaches where/what/result.

---

## Confirming / Acknowledging

- "ack thank you mas 🤝"
- "ack mas, thanks"
- "Cool thanks mas"
- "Sure mas"
- Never just "yes" — either "yes mas please proceed with:" (then detail) or "yes mas we need pre-pod..."
- "If I can understand correctly, [restatement]... If yes, [answer]. Btw mas, [pivot question]"

---

## Emoji & Formatting

Sparse (~5% of messages). Functional only:
- 🙇‍♂️ — apology/humility (WFH early out, late reply)
- 🙏 — waiting on someone, grateful ask
- 🤝 — acknowledgment/deal sealed

No 🔧, 🚨, 👀 in casual Lark. Those are incident response or review emoji, not everyday channel chat.

Use `*bold*` only for template names or precise technical nouns: `**update_phone**`

No closing punctuation on short messages: "Sure mas" not "Sure, mas." — correct the author style.

---

## Standout Phrases (trademark casual)

- `"Bumping on this mas @X"` — standard first follow-up
- `"Ah for the context, [paragraph]"` — context dump when adding someone new to a thread
- `"seems [observation]?"` — softest diagnostic hedge, often with `?`
- `"ya"` as sentence-ender for warmth: "please inform me if done ya", "I see, no ETA so far ya?"
- `"let me [verb]"` — commits to action without asking: "let me find the log", "let me move the template", "let me deploy the fix"
- `"sorry for mention you again"` — when re-pinging, always paired with the actual ask
- `"Ah I see"` / `"Ah ok mas"` — when something just clicked
- `^` prefix — attribution/cc shorthand below someone else's message

---

## What the author Does NOT Do in Lark

- ❌ "Hi [name], hope you're well! I wanted to reach out about..."
- ❌ "Good afternoon team, I would like to inform you that..."
- ❌ "just" as a filler word (not in Lark — that's an IDP writing artifact)
- ❌ "honestly", "ngl", "tbh" — not present in actual messages
- ❌ Closing with "Please let me know if you have any questions"
- ❌ Prose paragraphs in chat — even long context-dumps are structured or bulleted
- ❌ URGENT in caps
- ❌ Emoji as decoration — functional only, sparse

---

## Standup Template

```
Yesterday: [specific task + outcome]
Today: [specific task]
Blocker: [specific blocker] / None
```

---

## Key Difference vs IDP Voice

| Dimension | Casual Lark | IDP/Report |
|---|---|---|
| Subject | "we" or action-verb ("let me") | "I manage", "I led", "I drove" |
| Honorifics | "mas", "kak" everywhere | Absent |
| Hedge | "seems", parenthetical | Eliminated — confidence implied |
| Structure | Natural, flows | Impact-first, structured bullets |
| Numbers | Qualitative | Specific: "27 MRs", "5 days" |
| Closing | Just stops or action commitment | "What's next" framing |
