# Color science for products

A short, practical base of facts that explain why the rules in this skill exist. It lives in `data/color-facts.csv`. Each row has an id, a topic, the fact, what to do with it and a check you can run.

## How to use it

- When a rule feels arbitrary, find its row. The fact is the reason.
- When a user asks "why", answer with the fact and the check, in simple words.
- When you break a rule on purpose, name the row you are going against.
- Filter by topic to see all the facts that touch one decision.

## Topics

| Topic | Read it when |
|---|---|
| `perception` | A color looks off next to another one, or in a dark room |
| `spaces` | You build ramps, mix colors, or hit a gamut limit |
| `lightness` | You confuse lightness, brightness, chroma and saturation, or you read APCA |
| `warm-cool` | A palette feels too warm or too cold |
| `mixing` | Someone says "mix blue and yellow" |
| `print` | A color must be printed |
| `meaning` | A color carries a cultural or brand meaning |
| `data-viz` | You build a chart |
| `accessibility` | You prove contrast, color blindness or forced colors |

## Rules

1. A fact is not a style rule. Do not cite a row to defend a taste.
2. Do not add a row without a check. A fact you cannot test does not help the next reader.
3. Row ids stay stable. New rows take the next free number in their topic.
4. Write facts in your own words and keep them short.
