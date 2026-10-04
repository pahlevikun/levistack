# Rationalizations

If you did not watch the test fail, you do not know it tests the right thing. Violating the letter is violating the spirit. Rebuttals below; the loop is in `core/red-green-refactor.md` (linked from [SKILL.md](../../SKILL.md)).

| Excuse | Reality |
|--------|---------|
| Too simple to test | Simple code still breaks; the test is cheaper than a later debug |
| I'll test after | After-the-fact tests pass immediately and prove little |
| Same spirit, skip the ritual | Tests-after ask "what does this do?"; tests-first ask "what should this do?" |
| I already tried it manually | No record, not re-runnable, easy to miss cases |
| Deleting the spike wastes hours | Sunk cost. Unverified code is the waste |
| Keep as reference, then test | You will adapt it. That is tests-after. Delete the spike |
| Need to explore | Explore, throw away, start RED |
| Hard to test | The design is hard to use; simplify the seam |
| TDD slows me down | Faster than production debugging |
| Existing code has no tests | You are changing it; add a seam test for the behavior you touch |
| Just this once | That is the skip you will repeat |

**Allowed skips** (not rationalizations): throwaway prototype the user will discard; generated code you do not own; pure config/docs/static content; impractical bug path with a written why (`core/bug-fix-prove-it.md`).

Production-first code: delete and re-implement from tests. Do not "adapt while writing tests."
