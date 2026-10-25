# Support tickets and CRM

What customers reported, and when. Often the first record of a problem, before any alert fired.

## Where it lives

Zendesk, Freshdesk, Intercom, Jira Service Management, Salesforce (cases and accounts), HubSpot, support queues kept in Lark Base or Sheets (`lark.md`), shared inboxes, and CSV exports of any of these.

## How to search it

1. **Search by the symptom words** customers use, not the internal error name ("can't pay", "stuck on loading").
2. **Find the first report**: sort by created date. It often comes before the first alert.
3. **Count by day and by type** to see the spread and the start.
4. **Read the agent's notes and the escalation path**: they often hold the workaround and the engineering ticket id.
5. **In a CRM**, read the account or case history for the affected customer: config changes, plan changes, contract terms.
6. **CSV exports**: read them with a script that counts and groups. Do not paste the file.

## What good evidence looks like

- The first customer report, with its time, before the internal alert
- A spike in one ticket category that starts on a deploy date
- A case note with the workaround support used, and the engineering ticket it links

## Pitfalls

- **Personal data** is everywhere here. Return counts, categories and masked ids. Never names, emails, phone numbers or addresses (`rules/core/pii-logging.md`).
- **Customers describe symptoms.** A ticket is evidence of impact and timing, rarely of the cause.
- **Tagging is inconsistent.** Search by words as well as by tags.

## What to return

The system, the query or filter, counts by day and category, the first report's time, and masked ticket or case ids.
