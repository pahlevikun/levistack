# Collect feedback on proposal sections

Use when the user wants an interactive proposal review. Ordinary ADR drafting
continues without a review UI. The bundled offline packet replaces a local server:
no network requests, external libraries or database are needed.

```sh
python3 scripts/review_packet.py proposal.md --output proposal-review.html
```

Open the resulting HTML locally. A reviewer can assess each heading, write comments
and download proposal-feedback.json. The packet contains a source SHA-256 and
section identifiers. It does not update the source, submit approval or preserve
comments after closing unless the reviewer downloads them. Headings inside fenced
code stay in their original section. The tests live in scripts/test_review_packet.py.

Before applying comments, recompute the source hash. If it differs, match sections
against the new text and resolve stale comments rather than applying by array
position. Separate questions, requested revisions and approvals. Only the actual
owner can accept a decision; a downloaded Agree label is feedback, not a release
or deployment authorization. Keep sensitive proposals and feedback local.

Present proposed edits with their rationale, make authorized changes, then produce
a new packet for another round only when needed. Preserve accepted decision history.
If the environment cannot open local HTML, provide the same section-ID table in
Markdown. No browser launch or server startup is implicit in creating the packet.
