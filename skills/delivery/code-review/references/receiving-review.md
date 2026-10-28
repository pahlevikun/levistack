# Receiving code review

Technical evaluation, not emotional performance. **Verify before implementing.**

## Response pattern

1. **Read** — complete feedback without reacting  
2. **Understand** — restate requirement or ask  
3. **Verify** — check against codebase reality  
4. **Evaluate** — sound for *this* codebase?  
5. **Respond** — technical acknowledgment or reasoned pushback  
6. **Implement** — one item at a time, test each  

## Forbidden responses

Never: "You're absolutely right!"; "Great point!"; "Let me implement that now" (before verification).

Instead: restate the requirement, ask questions, push back with reasoning, or start working.

## Unclear feedback

If any item is unclear: **stop** — do not implement partial fixes. Items may be related; partial understanding → wrong implementation.

## Source-specific handling

**Human partner:** trusted after understanding; still ask if scope unclear; no performative agreement.

**External reviewers:** before implementing — technically correct here? breaks anything? reason for current code? platform/version gaps? full context?

If wrong: push back. If hard to verify: state what you need. If conflicts with partner decisions: stop and discuss with partner first.

## YAGNI for "professional" features

If reviewer wants a full implementation: grep for usage. Unused → propose removal (YAGNI). Used → implement properly.

## Implementation order

1. Clarify unclear items first  
2. Blocking (breaks, security) → simple fixes → complex fixes  
3. Test each fix; check regressions  

## Push back when

Suggestion breaks behavior; reviewer lacks context; YAGNI; wrong for this stack; legacy/compatibility; conflicts with architectural decisions.

Use technical reasoning, specific questions, tests/code; escalate architectural conflicts to your partner.

## Acknowledging correct feedback

✅ "Fixed. [what changed]" / "Good catch — [issue]. Fixed in [location]." / just fix in code  

❌ gratitude phrases, "Thanks for catching that"

## Correcting wrong pushback

✅ "You were right — I checked [X]. Implementing now." (factual, brief)  

❌ long apology or re-litigating the pushback

## GitHub thread replies

Reply in the inline comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## Bottom line

External feedback = suggestions to evaluate, not orders. Verify. Question. Then implement.
