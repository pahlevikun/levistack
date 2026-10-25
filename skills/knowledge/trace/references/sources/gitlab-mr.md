# GitLab merge requests and issues

## What this source holds

- The MR description, often from a template with "why" and "how to test"
- Discussions and line notes, resolved and unresolved
- Approvals, pipelines per commit, and the merge commit
- Linked issues, epics and milestones
- MR versions: what changed between pushes

## How to search it

```bash
# The MR behind a commit
glab mr list --state all --search '<sha or words>'
glab api "projects/:id/repository/commits/<sha>/merge_requests"

# The full MR with comments
glab mr view <iid> --comments

# Every discussion thread, including line notes and resolved threads
glab api "projects/:id/merge_requests/<iid>/discussions?per_page=100" --paginate

# The versions (each push), to see what reviewers saw
glab api "projects/:id/merge_requests/<iid>/versions"

# Linked issues and the issue's own notes
glab api "projects/:id/merge_requests/<iid>/closes_issues"
glab issue view <iid> --comments

# Pipelines for the MR, to see what failed and when
glab api "projects/:id/merge_requests/<iid>/pipelines"
```

`:id` is filled from the current repo by `glab`. For another project, use its URL-encoded path.

## What good evidence looks like

- An MR description that names the problem and the chosen approach
- A resolved thread where a reviewer asked for a change and the author agreed or pushed back
- A linked issue or epic with the product reason
- A failed pipeline right before a "fix" commit

## Pitfalls

- **Squash on merge** leaves one commit. The MR holds the real history.
- **System notes** (label changes, pushes) are noise. Filter them out, but keep "mentioned in" notes, which link other MRs and issues.
- **Self-hosted GitLab** may need `glab auth login --hostname <host>`. If it fails, report the gap.

## What to return

MR iid, title, author, merge date, the quoted "why" text, decisive threads with path and line, linked issues, and the pipeline result that matters.
