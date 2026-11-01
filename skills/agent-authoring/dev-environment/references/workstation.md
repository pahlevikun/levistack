# Workstation

Back up or apply a Mac developer workstation. This skill ships the scripts, the directory layout, and a seed of the snapshot repo. The layout is in `structure.md`.

The snapshot repo is `$LAPTOP_SETUP_ROOT`. When that variable is unset, use `$HOME/laptop-setup`.

The snapshot holds lists and config, not app binaries and not the contents of git repos. `private/` is not in the seed. Never copy a private key into the seed.

## First run

If the snapshot repo does not exist, or it has no `apply.sh`, run `scripts/init-repo.sh` from this skill.

That script:

1. Copies `seed/` into the snapshot repo. Existing files in the repo stay. Missing files are added.
2. Creates every directory listed in `seed/structure/home-dirs.txt` under `$HOME`.
3. Runs `git init` when the destination has no `.git`.

Then continue with backup or apply.

## Scripts

| Script | Does |
|---|---|
| `scripts/init-repo.sh` | Create or update the snapshot repo from `seed/` |
| `scripts/snapshot` | Run init, then the repo's `scripts/snapshot.sh` |
| `scripts/apply` | Run init, then the repo's `apply.sh` |

The seed also includes `apply.sh`, `Brewfile`, `scripts/snapshot.sh`, `scripts/upsert.py`, `scripts/clone-repos.sh`, `scripts/install-editor-extensions.sh`, and `scripts/install-chrome-extensions.sh`.

## Backup

Refresh the snapshot from the live machine, then show the diff. Do not commit unless asked.

1. Run `scripts/init-repo.sh` if the snapshot repo is missing.
2. Read the live machine before copying: shell config, editor extensions and local plugins, Homebrew package names, and language pins.
3. Run `scripts/snapshot`. It keeps variable names and replaces token, key, and password values.
4. Copy SSH config and public keys only. Never copy a private key.
5. Show `git status` and `git diff`. If a secret is in the diff, redact it before you report.
6. Commit or push only after a yes.

Report what changed: new packages, new editor plugins, and any secret fields you redacted.

## Apply

Upsert onto `$HOME`. Existing files, packages, plugins, keys, and running agents stay. The snapshot fills gaps.

1. Run `scripts/init-repo.sh` if the snapshot repo is missing.
2. Run `scripts/apply` with `--dry-run` first if you are unsure. Apply only after a yes. Add `--with-clones` or `--with-chrome` only if asked.
3. Confirm the script upserts: skip a file that already exists, merge missing JSON keys, union the shell plugin list, install missing Homebrew packages without removing extras, clone a plugin or a git repo only when the destination is missing, and do not stop a running agent.
4. If `apply.sh` replaces a file wholesale, stop. Do not overwrite the machine to "fix" it.
5. After apply, list the logins that are still manual. Name the tool. Do not print a token or a key.

## Output

Backup: the snapshot path, what changed, and any secret fields you redacted. Apply: what was added, what was left in place, and the manual logins still open.
