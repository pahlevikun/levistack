# GitHub pull requests and issues

## What this source holds

- The PR body: the stated goal, the "why", screenshots, test notes
- Review comments on lines, and the review summary (approved, changes requested)
- The discussion timeline: pushes, force-pushes, label changes, linked issues
- Issues the PR closes, and their own discussion
- CI checks on each commit of the PR

## How to search it

```bash
# The PR behind a commit
gh pr list --state all --search '<sha>' --json number,title,url
gh api repos/{owner}/{repo}/commits/<sha>/pulls --jq '.[].number'

# The full PR: body, reviews, comments, linked issues
gh pr view <n> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews,commits

# Line comments (review threads), which `gh pr view` does not show in full
gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate --jq '.[] | {path, line, user: .user.login, body}'

# The issue timeline: who linked, closed, or reopened it, and when
gh api repos/{owner}/{repo}/issues/<n>/timeline --paginate

# Search PRs and issues by words
gh search prs --repo {owner}/{repo} '<words>' --json number,title,url
gh search issues --repo {owner}/{repo} '<words>' --json number,title,url
```

## What good evidence looks like

- A PR body with a "why" or "context" section
- A reviewer asking "why not X?" and the author's answer
- A linked issue with the user report or the business reason
- A reverted PR and the PR that re-applied it

## Pitfalls

- A **force-push** can erase the commits reviewers saw. Read the timeline.
- **Review comments on outdated lines** still count. They often hold the real decision.
- **Private forks or deleted branches** can hide history. Say so as a gap.
- `gh` needs auth. If `gh auth status` fails, report the gap.

## What to return

PR number, title, author, merge date, the quoted "why" text, the decisive review comments with their path and line, and linked issues.
