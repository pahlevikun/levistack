# GitLab and GitHub

What to collect from each forge: MRs or PRs the user **raised**, **reviewed** (approvals, changes requested), **commented on**, and **reacted to**, plus pushes and merges. Use the hosts and usernames from the config; for a forge that is not there, take the host from `git remote get-url origin` in the repos the machine step found.

Timestamps from both APIs are UTC. Convert to the local day before deciding which day an event belongs to, or late-evening work lands on the wrong date. To turn the unix bounds from `collect.mjs range` into UTC strings:

```bash
node -e 'for (const t of process.argv.slice(1)) console.log(new Date(t*1000).toISOString())' <startTs> <endTs>
```

## GitLab (`glab`)

`glab mr list` has no date filters, so use the REST API through `glab api`. Add `--hostname <host>` for self-managed instances. Dates for `after` and `before` are exclusive: pass the day before `start` and the day after `end`.

```bash
HOST=git.example.com
ID=$(glab api user --hostname $HOST | jq .id)

# everything you did: pushes, opened/merged MRs, approvals, comments, issues
glab api "users/$ID/events?after=<start-1>&before=<end+1>&per_page=100" --paginate --hostname $HOST \
  | jq -r '.[] | "\(.created_at[0:16]) \(.action_name) \(.target_type // "push") !\(.target_iid // "") \(.target_title // .push_data.commit_title // "") [project \(.project_id)]"'
```

`action_name` values to look for: `opened`, `accepted` (merged), `approved`, `commented on`, `pushed to`, `pushed new`, `closed`. The event carries only `project_id`; name a project with `glab api projects/<id> --hostname $HOST | jq -r .path_with_namespace`.

```bash
# MRs you authored or are a reviewer on, touched in the window
glab api "merge_requests?scope=all&author_username=<user>&updated_after=<startIso>&updated_before=<endIso>&per_page=50" --hostname $HOST
glab api "merge_requests?scope=all&reviewer_username=<user>&updated_after=<startIso>&updated_before=<endIso>&per_page=50" --hostname $HOST

# reactions you gave on a specific MR (there is no "my reactions" feed, so check the MRs you found)
glab api "projects/<id>/merge_requests/<iid>/award_emoji" --hostname $HOST \
  | jq --arg u "<user>" '[.[] | select(.user.username==$u)]'
```

For the comments themselves, `glab api "projects/<id>/merge_requests/<iid>/notes?per_page=100"` and keep `author.username == <user>` with `created_at` in the window; system notes (`"system": true`) are not yours.

Merged MRs by the user come from `accepted` events or from `state=merged` on the authored list. Report "merged" only for those.

## GitHub (`gh`)

```bash
USER=<login>
R="2026-10-02..2026-10-04"      # local dates; search takes a closed range

gh search prs --author $USER   --updated "$R" --json number,title,repository,state,url
gh search prs --reviewed-by $USER --updated "$R" --json number,title,repository,state,url
gh search prs --commenter $USER   --updated "$R" --json number,title,repository,state,url
gh search prs --author $USER   --merged   --merged-at "$R" --json number,title,repository,url
```

Search tells you which PRs were involved, not what you did on them. For the detail:

```bash
# your reviews on one PR (state: APPROVED, CHANGES_REQUESTED, COMMENTED)
gh api repos/<owner>/<repo>/pulls/<n>/reviews --jq '.[] | select(.user.login=="'$USER'") | {state, submitted_at}'

# your activity feed: pushes, PRs, reviews, review comments, issue comments (last 90 days, 300 events)
gh api "users/$USER/events?per_page=100" --paginate \
  --jq '.[] | select(.created_at >= "<startUtc>" and .created_at <= "<endUtc>") | {type, repo: .repo.name, at: .created_at}'

# reactions you gave on a PR or issue
gh api repos/<owner>/<repo>/issues/<n>/reactions --jq '.[] | select(.user.login=="'$USER'") | {content, created_at}'
```

The events feed shows private activity only when you are authenticated as that user.

## Turning it into bullets

- Raised: `!42 retry flaky upload (opened, still in review)`. Say merged only when it merged.
- Reviewed: name the MR, the repo, the outcome (approved, left comments, requested changes). Several comments on one MR are one bullet.
- Reactions are colour, not work. Mention one only if it closed a loop ("thumbs-up on the rollout plan").
- Join each MR to its ticket key and to the machine-step commits; one piece of work is one bullet.
