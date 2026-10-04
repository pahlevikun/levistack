# Seams: where tests go

A **seam** is the public boundary you observe without reaching inside: HTTP handler, package API, module export, UI via role/text, message contract.

Tests live at seams. Code behind the seam may change entirely; tests should not.

## Good vs bad

| Good | Bad |
|------|-----|
| "user can checkout with a valid cart" through the checkout API | Asserting a private helper was called |
| Behavior via exported function / handler | Querying the database instead of the interface that owns that write |
| Test still passes after an internal rename | Test fails when you rename an unexported function |

Warning sign: refactor with unchanged behavior, tests go red. Those tests were coupled to implementation.

## Agree the seams first

You cannot test everything. Before the first test in **plan** or **loop**:

1. Name the public interface under change.
2. List the seams you will test (usually one or two for a slice).
3. Confirm with the user when the interface is new or controversial.
4. Prioritize critical paths and complex logic, not every edge.

Ask: "What is the public interface, and which seams should we test?"

## Prefer state over interactions

Assert on outcomes (status, returned value, visible UI, persisted record via the owning API). Do not assert call graphs of internal collaborators.

Fakes (in-memory stand-ins) beat interaction mocks. Mocks are isolation tools, not the thing under test. Full mock gates: `legacy/catalog-anti-patterns.md` (linked from [SKILL.md](../../SKILL.md)).

## DAMP in tests

Production code prefers DRY. Tests prefer **DAMP** (descriptive, meaningful phrases): a test should read as a spec without tracing a tower of shared helpers. Shared setup is fine when it hides noise, not when it hides what is asserted.
