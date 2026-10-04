# Plain Comms — Email, Letter, Announcement

Use this file for **email**, **letter**, and **announcement** modes only.
The English and Indonesian **language** bar (simple vocab, one intention, natural grammar, Indo-US false friends) lives in [core.md](../core.md). Do not skip core.

Layout overlay for these three formats: first sentence is the know/do. Then only what they need to act.

## Techniques

Load [email-comms.md](../techniques/email-comms.md) for structure (maps to `email`, `letter`, `announcement` use cases).

Load [natural-writing.md](../techniques/natural-writing.md) on rewrite passes.

Load locale technique from [core.md](../core.md) when `language` matches — see [techniques/README.md](../techniques/README.md).

---

## Before you write (30 seconds)

Answer this in one sentence, in simple words:

> After they read this, what should they **know** or **do**?

That sentence is line 1 of the draft. Everything else must earn its place.

Then write:

1. **Intention** — the know/do sentence
2. **Need-to-know** — only facts they need to act (who, when, where, link)
3. **Ask or next step** — one clear action, owner, and time if it exists
4. **Stop** — no recap, no "let me know if you have any questions" unless a real question is open

---

## Indo-US tone

Write for a reader who is fluent in work English but is not a native US office speaker, and for a US reader who should never feel the text is stiff or "translated".

**From US writing, keep:**
- First sentence is the point. No warmup.
- Short paragraphs (1–3 sentences).
- Concrete verbs: send, need, start, stop, join, check, fix, wait.
- Dates and times with timezone (`Tue 16 Sep, 14:00 WIB`).

**From Indonesian writing, keep:**
- Warm, not cold. Use the person's name.
- Thank once when it is real. Do not thank in every paragraph.
- Polite without being formal: "Could you send the file today?" not "Kindly be informed that we request..."
- Internal chat still uses `mas` / `kak` when addressing people. Email to external people uses their name only.

**Both sides agree on:**
- Common words only
- Natural grammar (complete sentences, correct agreement)
- One intention per sentence

### Do not mix these false friends

These words confuse one side of an Indo-US team. Never use them with the other meaning.

| Do not write | Why it confuses | Write instead |
|---|---|---|
| revert (as "reply") | US reads this as "undo". Common in ID/SG/IN English for "reply" | reply / get back to you |
| kindly | Sounds stiff or like a template. US rarely uses it in email | please / just ask directly |
| please be informed / please be advised | Formal memo. Feels copied | just state the fact |
| do the needful | Indian-English set phrase. Unclear to US | say the exact action |
| prepone | Not used in US English | move earlier / move to [day] |
| out of pocket | US = unavailable. ID may hear "paying myself" | away / offline until [time] |
| table this | US = delay it. UK = put it on the agenda | delay this / discuss this in the meeting |
| circle back / loop in / touch base | US office slang. Easy to misread | I'll reply / I'll add [name] / let's talk |
| bandwidth / capacity (for people) | Abstract. Sounds like infra | time / can take this / too busy this week |
| going forward | Filler | from [date] / from now |
| as per / as per my last email | Cold and scolding | as we agreed / as I sent on [date] |
| utilize / facilitate / leverage / commence | Fancy synonyms | use / help / use / start |
| whilst / amongst | British, uncommon in this team | while / among |
| aforementioned / hereby / thereof | Legal tone | this / that / the [noun] |

### Words both sides already know — prefer these

ask, tell, need, send, check, start, stop, wait, join, share, fix, delay, cancel, today, tomorrow, next week, blocker, owner, deadline, update, meeting, file, link, please, thanks.

If you would explain a word to a teammate, do not use it. Pick the known word.

---

## Sentence craft

**One intention per sentence.** The subject and the verb carry the point. Extra facts go in the next sentence.

| Weak (stacked or fancy) | Strong (one intention, common words) |
|---|---|
| I wanted to reach out in order to align on the upcoming rollout and also loop in infra. | I need a yes/no on the Tuesday rollout. I will add the infra team after we agree. |
| Kindly revert with your availability at your earliest convenience. | When can you meet this week? Tue 14:00 or Wed 10:00 WIB both work for me. |
| Please be informed that the channel will be used for announcements going forward. | From Monday, this channel is for announcements only. |

**Natural grammar (default for all new drafts):**
- Complete subject–verb–object: "The deploy needs a review today."
- Correct agreement: "it needs to happen", not "it need to happen"
- No telegram fragments in email or letters: not "Need review. Tomorrow. Thanks."
- Chat and announcements may be shorter, but still a real sentence: "Standup moves to 10:00 WIB from Monday."

Old IDP files used some Indonesian-English grammar quirks. **Do not copy those into new writing** unless the user pastes an old IDP and asks to match it.

**Warmth without fluff:**
- Yes: "Thanks mas @Andi, I will check the log."
- No: "Hope you're doing well! Just a quick one when you get a chance..."

---

## Email

### New email

```
Subject: [noun + action or outcome] — not "Update" or "Question"

Hi [Name],

[Intention: what I need you to know or do.]
[1–2 short sentences of need-to-know context.]
[One ask, with time if it exists.]

Thanks,
the author
```

Subject patterns that work:
- `Need review on CUI SMS template by EOD`
- `Tue 16 Sep 14:00 WIB — CUI go-live huddle`
- `Following up: production SMS still on old template`

### Reply

1. Answer first. If they asked three things, answer in the same order, short lines.
2. Then add context only if the answer is not enough alone.
3. No greeting in a tight reply thread if the thread is already moving — same as Lark. For a cold or external thread, keep `Hi [Name],`.
4. Do not quote the whole mail. Quote one line only when the ask would be unclear.

Reply skeleton:

```
Hi [Name],

[Direct answer.]
[One extra fact if needed.]
[What I will do next, or what I need from them.]

Thanks,
the author
```

### Follow-up (still no guilt trip)

```
Hi [Name],

Checking in on [the exact ask] from [day].
I still need [the thing] by [time] so I can [why].

Thanks,
the author
```

Internal Lark follow-up stays in conversation mode (`Bumping on this mas @X`). Email follow-up uses the skeleton above.

### Decline or delay

Be clear in sentence 1. Offer one other option if you have one. Do not over-apologize.

> I cannot join Thursday's call. I can do Friday 10:00–11:00 WIB, or I can send written notes before Thursday.

### Anti-patterns (email)

- ❌ "I hope this email finds you well"
- ❌ "Just circling back"
- ❌ "Please revert"
- ❌ "As per my last email"
- ❌ "Please let me know if you have any questions" as a closer when nothing is open
- ❌ Hiding the ask in paragraph 3

---

## Letter

Use for a formal letter, recommendation, cover note, or `surat` that will be read slowly (HR, partner, university, printed PDF). Still simple words. Still one intention per paragraph.

```
[Date]

Dear [Name / Bapak / Ibu / Hiring team],

[Why I am writing — one sentence.]

[Facts. 1–2 short paragraphs. Numbers where you have them. No adjectives without evidence.]

[The ask, or a clean close. What they can do next.]

Sincerely,
the author
```

Register:
- External / HR / official: `Dear ...`, `Sincerely`. No `mas`/`kak`. No slang.
- Internal recommendation that will stay in the company: still complete grammar, still simple words. You may say "I work with [Name] on [project]".

Recommendation body pattern:

> I am writing to recommend [Name] for [role].
> On [project], they [specific thing they did]. That [result with a number if you have one].
> I would work with them again on a similar problem.

Do not write a Victorian letter. Do not write a LinkedIn toast.

---

## Announcement (channel, team, company)

A broadcast. Many people will skim. First line is the news.

```
[News in one sentence.]

Who this affects: [teams / roles]
What to do: [action, or "nothing, this is FYI"]
When: [date + time + timezone]
Where / link: [channel, doc, ticket]
Who to ask: @[owner]
```

Channel post (Lark/Slack) can drop labels if the lines are already clear:

```
From Monday 15 Sep, standup moves to 10:00 WIB.
Same channel. Drop your update in the thread before 10:00 if you cannot join.
Questions: mas @the author
```

Company-wide or cross-org: keep the labels. Add one sentence of why only if people will resist the change.

Incident / change window:

```
Tonight 22:00–23:00 WIB we will restart [service] in staging.
Expect login errors during that hour in staging only. Production is not in this window.
Owner: mas @Name. I will post here when it is done.
```

### Announcement vs conversation

| | Conversation | Announcement |
|---|---|---|
| Audience | one thread, few people | a channel or a whole team |
| Opening | no greeting in-thread | news first; "Hi team" only for a new top-level post |
| Honorifics | `mas`/`kak` on requests | owner named once; do not mas-tag the whole company |
| Length | 50–200 chars typical | as short as the 4 facts allow |
| Close | stop, or one question | who to ask |

WhatsApp / Slack blast, "FYI team", "please announce this" → announcement.
Thread reply, DM, standup → conversation (`daily-conversation.md` in this folder).

---

## Worked rewrites

**Email reply**

Before:
> Hi, hope you're doing well! Just wanted to circle back on the below and kindly revert with your thoughts on the proposed cadence at your earliest convenience.

After:
> I can do the weekly check-in on Tuesdays at 14:00 WIB.
> If Tuesday is hard, Wednesday 10:00 WIB also works.

**Letter open**

Before:
> I am writing to formally express my interest in exploring potential opportunities for collaboration with your esteemed organization.

After:
> I am writing to ask if we can set up a 30-minute call next week about the merchant onboarding API.

**Channel announcement**

Before:
> Hi team, I wanted to align everyone going forward on a small process change that should hopefully streamline our standup cadence.

After:
> From Monday, standup is 10:00 WIB in this channel.
> If you will miss it, post your update in the thread before 10:00.
