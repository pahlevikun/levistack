# Worked example — single-commit branch with error-code change

This walks through one realistic invocation end-to-end so the agent can see the full transformation.

## Input

**Branch:** `feat/PROJ-123-profile-contact-flow-header`
**Base:** `origin/master`
**Commits on branch:**

```
3f9a1c2 enhancement(profile:commit): [PROJ-123] update verification flow handling and improve credential validation in commit stage, implement phone number validation and normalization utilities
```

## Step 1 — discover commit set

```bash
git log --no-merges --reverse --format='%H%x09%s%x09%an' origin/master..HEAD
# 3f9a1c27b0e...    enhancement(profile:commit): [PROJ-123] ...    Jane Doe
```

One commit, one author, one ticket (`PROJ-123`).

## Step 2 — pull diff signals

The agent runs `git show 3f9a1c2 -- workflow/.../errors/errors.go` and sees:

- `ErrOTPChallengeInvalid`: `http.StatusBadRequest` → `http.StatusUnprocessableEntity` (status flip)
- `ErrTokenInvalid`: `http.StatusBadRequest` → `http.StatusUnprocessableEntity` (status flip)
- `ErrCredentialMismatch`: **new** at 422 with code `UPDATE_PROFILE_CREDENTIAL_MISMATCH`

In `task/verification_check.go` it sees new `headers.Get("X-Verify-Flow")`, `headers.Get("X-Verify-Country-Code")` and a new `validateCredentialFormat` helper that returns `ErrInvalidField`.

In `task/commit_credentials.go` it sees a new switch on `verificationOutput.Flow` with a `default` branch returning `ErrInternalError`.

`CHANGELOG.md` is **not** in the diff.

## Step 3 — extracted signals

| Signal | Value |
|---|---|
| Ticket | `PROJ-123` |
| Author | `jane.doe@example.com` → `@jane.doe` |
| Conventional prefix | `enhancement` → ✨ New feature |
| New error code | `UPDATE_PROFILE_CREDENTIAL_MISMATCH` (422) |
| Changed status codes | `OTP_CHALLENGE_INVALID` 400→422, `TOKEN_INVALID` 400→422 |
| New required headers | `X-Verify-Flow`, `X-Verify-Country-Code` |
| New routes | none |
| CHANGELOG | not updated |
| Breaking? | yes — new required headers + status codes flipped |

## Step 4 — output

````markdown
### Description

Updates the `update-profile` credentials commit flow to align verification header handling with the identity-proxy contract, and tightens both pre-commit and post-commit credential validation.

**Main changes:**

- Require `X-Verify-Flow`, `X-Verify-Number` + `X-Verify-Country-Code` (phone) or `X-Verify-Email` (email) headers on `POST /v1/update-profile/contact/commit`.
- Add `validateCredentialFormat` step in `credentials-check` and `contact/verification-check` (rejects malformed phone/email via `utils.IsValidPhoneNumber` / `utils.IsValidEmail`).
- After the identity commit, compare returned credential against the request; mismatch returns the new `ErrCredentialMismatch` (422).
- `VerificationCheckOutput` now carries `Flow`; `CommitCredentials` switches on it instead of inferring from `Phone != ""`.
- Flip `OTP_CHALLENGE_INVALID` and `TOKEN_INVALID` from 400 → 422 (semantic-content failures).
- Add shared `utils.NormalizePhoneNumber` / `IsValidPhoneNumber` / `IsValidEmail` with unit tests.

**Error code summary:**

| Code | Status | Change |
|---|---|---|
| `UPDATE_PROFILE_CREDENTIAL_MISMATCH` | 422 | **NEW** — the identity service returned a credential that disagrees with the requested update |
| `UPDATE_PROFILE_OTP_CHALLENGE_INVALID` | 400 → 422 | semantic-content failure |
| `UPDATE_PROFILE_TOKEN_INVALID` | 400 → 422 | now also raised on missing/mismatched `X-Verify-Flow` |
| `UPDATE_PROFILE_BAD_REQUEST` | 400 | now also raised by the new `validateCredentialFormat` step |
| `UPDATE_PROFILE_INTERNAL_ERROR` | 500 | now also raised by `CommitCredentials` on unrecognized `Flow` |

### Authors

@jane.doe

### Relevant Tickets

- Closes [PROJ-123](https://jira.example.com/browse/PROJ-123)

### Checklist

- [ ] If not WIP or draft, run/re-run `static_checks` job to perform checks and assign the MR
- [x] I have read and followed [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have updated [CHANGELOG.md](../CHANGELOG.md) under `"## Unreleased"` section
- [x] My code follows the project's code style and conventions
- [x] I have performed a self-review of my own code
- [x] I have added/updated unit tests that prove my fix/feature works
- [x] All new and existing tests pass locally

### Type of Change

- [x] ✨ New feature (non-breaking change which adds functionality)
- [x] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)

> **Breaking notes for FE/BFF:**
> - Three new required verification headers on `POST /v1/update-profile/contact/commit`.
> - `OTP_CHALLENGE_INVALID` and `TOKEN_INVALID` now return HTTP 422 instead of 400 (codes unchanged).
> - New `CREDENTIAL_MISMATCH` (422) is now possible after a successful identity call if the returned phone/email disagrees with the request.

### Screenshots / Logs / CURL (if applicable)

```bash
curl -X POST http://<service-host>/v1/update-profile/contact/commit \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 10000001" \
  -H "X-Account-Id: acct_1000042" \
  -H "Authorization: Bearer <verify-token>" \
  -H "X-Verify-Flow: update_phone" \
  -H "X-Verify-Number: 5550100123" \
  -H "X-Verify-Country-Code: +1" \
  -d '{"verification_token":"<RS256 JWT>","session_id":"sess-...","user_id":"10000001","phone":"+15550100123"}'
```

```json
{
  "status": "error",
  "error": {
    "code": "UPDATE_PROFILE_CREDENTIAL_MISMATCH",
    "message": "identity service returned a credential that does not match the requested update"
  }
}
```

### For Reviewers

**Review Guidelines:**

- Focus on functionality, code quality, tests, and documentation
- Be constructive and specific in feedback
- Review within 24-48 hours (urgent MRs: same day)

**Reference:**

- [Contributing Guide](../CONTRIBUTING.md)
````

**Follow-ups:**

- CHANGELOG entry missing — propose: `- [PROJ-123] update-profile/contact: enforce X-Verify-Flow header, add CredentialMismatch (422); flip OTP_CHALLENGE_INVALID and TOKEN_INVALID to 422`.
- `workflow/update-profile/v1/contact/test/data/README.md` still lists the two flipped errors at HTTP 400 and doesn't mention the new headers — update before merge.
- Marked 💥 Breaking change because of the new required headers and the 400→422 migration.

---

## What this example demonstrates

- A single commit can still warrant a `Main changes` list — group by intent (header contract / format validation / mismatch guard / status flip / utils).
- The error-code table replaces what would otherwise be three paragraphs of prose.
- Curl headers are taken from the diff (`X-Verify-Flow`, `X-Verify-Country-Code`), not from memory.
- The CHANGELOG checkbox stays unchecked because the diff doesn't touch CHANGELOG.md — and the missing entry shows up in follow-ups with a proposed line.
- `static_checks` stays unchecked because it's CI-side; the agent can't verify it from the diff.
