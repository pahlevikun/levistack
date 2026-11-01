# Watch

Stay with one pull request or merge request until it is clean. Do not stop after one green check while a thread is still open.

## Host

Detect the host from the URL the user gave, or from `git remote get-url origin` when they did not.

| Host | Read status with | Threads |
|---|---|---|
| GitLab (`gitlab.com`, a self-hosted GitLab, or `glab`) | `glab mr view` and the MR scripts in this skill | Open discussions from the MR metadata |
| GitHub (`github.com` or `gh`) | `gh pr view` for state, draft, mergeability, and checks | Unresolved review threads via `gh api graphql` |

A GitHub URL does not use the GitLab draft-note scripts. A GitLab URL does not use `gh`.

## Each pass

Re-read live status at the start of every pass. Do not act on a status from an earlier pass.

1. Confirm the request number, the branch, and the base. If it is a draft, say so and continue watching checks and threads. Do not mark it ready.
2. Wait for pending checks to finish. Watch them rather than polling in a tight loop.
3. Read new comments and unresolved threads. A bot summary is a lead. Confirm the finding against the current code before changing anything.
4. Fix a real issue that is inside this request. Run the narrowest check that proves the fix. Do not push unless the user already said to push.
5. Dismiss a thread only when the current code or the generated artifact already answers it. Say why. Leave a thread open when it is waiting on the user, or when the topic is security, privacy, auth, billing, data, migration, or concurrency and you would be guessing.
6. Resolve a thread only after the fix is verified and you have permission. A local commit is not enough to claim a remote thread is done.

## Stop

Stop only when all of these are true:

- Required checks are passing, or the project intentionally skips them.
- No actionable comment is left.
- No unresolved review thread is left, except one you have named as waiting on the user.

Report the latest head SHA, the check names and results, the unresolved thread count, the tests you ran, and any local files you did not touch.
