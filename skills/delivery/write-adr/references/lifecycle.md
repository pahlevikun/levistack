# Maintain an ADR's history

1. Read the repository's status vocabulary and the record's current status. Find its index and any incoming or outgoing supersession links.
2. Confirm the decision event from an approval record, named owner, or explicit user instruction. A request to draft a replacement does not itself accept either record.
3. For a status update, change only the authorized status metadata, date, and explanation. Preserve the earlier decision text so the historical reason remains readable.
4. For a replacement, create a new record in the local format. Link the old record to the new one and the new record to the old one. State what changed and why. Update the index if one exists.
5. Reopen both records and the index. Verify link targets, numbering, status, and which decision currently governs. If acceptance evidence is absent, leave the replacement proposed and report the gap.

Do not send approval requests, notify teams, create tickets, or implement the decision unless the user separately asked for those actions.
