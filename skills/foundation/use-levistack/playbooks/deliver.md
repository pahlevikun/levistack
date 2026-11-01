# Deliver

**Step 7**, the last pass on every router reply. It is always this session finishing the reply, after the chain, after a one-shot, or after a subagent returns. It is not another spawn.

The proof lines from [prove.md](prove.md) are protected. Nothing below may shorten them away.

## 1. polyglot-copywriter (when there is prose for people)

Run `polyglot-copywriter` on draft text a person will read: an MR or PR description, a review comment, an email, a chat message, a ticket, a doc or README section, an incident update.

Run it on that prose only. Commands, ids, paths, code and payloads stay exact.

Skip it when the reply is only findings, skill names, commands, ids or notes for the agent.

## 2. output-savers (always, last)

Read [output-savers](../../../engineering/output-savers/SKILL.md) with an explicit job from [auto-detect.md](../../../engineering/output-savers/references/auto-detect.md):

| Reply shape | Job |
|---|---|
| Prose for a person (already through polyglot-copywriter) | 14: do not compress |
| Technical answer or debugging | 13: pilot style |
| Steps the user will run | 12: astronaut style |
| Proposed outward action, proof, rollback | Safety override: full sentences, keep every proof line |

If compression would drop an id, a proof line, a rollback step or a "not verified" line, keep the long form.

## Report shape

End with what ran, in one line per skill, and what is left or was not done. No closing pleasantries.
