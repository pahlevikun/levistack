# Publishing transport gate

Good copy and assets can still fail in the queue if a scheduler stores escaped text or platform markup differently from your source file.

## Before scheduling

Inspect the exact payload that will be sent:

- Paragraph breaks are real newline characters.
- The content has no literal `\n` escape sequence in the stored body.
- Raw `<p>`, `<br>`, or editor markup is absent unless the API requires HTML.
- Spacing between hook, body, example, and CTA is intentional.
- Media files match the correct account and platform.
- Date and timezone are explicit.
- Alt text and link targets match the delivered asset paths.

Pair with [formats](formats.md) for dimensions and publication-boundaries for rights (see SKILL.md router).

## After scheduling

Fetch the post back from the scheduling API. Inspect stored content, not only the local draft.

Release blockers:

- Literal escape sequences in the body.
- Collapsed paragraphs.
- HTML tags that will show as text on the platform.
- Missing or wrong media attachment.
- Wrong profile or integration.
- Duplicate post at the same slot without intent.

## Safe correction when posts are immutable

When the API cannot edit a scheduled post:

1. Create the corrected replacement as a draft.
2. Fetch it back and verify content, media, account, and date.
3. Move the defective scheduled item to draft or cancel per platform rules.
4. Promote the verified replacement to the queue.
5. Fetch the queue again and confirm one active post at that slot.

Do not delete the original without a record. Do not retry an ambiguous write before checking whether it already succeeded.

## Receipt

Log scheduler name, post id, fetch timestamp, and any mismatch found. Attach screenshot or API snippet when the platform allows.
