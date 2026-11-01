# Workstation snapshot

Example seed for `dev-environment`. First run copies this folder to `$HOME/laptop-setup` (or `$LAPTOP_SETUP_ROOT`). Paths in the seed use `$HOME`. Apply expands that placeholder in plist and JSON files when it copies them.

Nothing here is a real machine. Tokens, private keys, and session files stay out. `private/` is gitignored.

## Restore

```bash
# created by scripts/init-repo.sh when the snapshot repo is missing
cd "$HOME/laptop-setup"
./apply.sh --dry-run
./apply.sh -y
```

Apply is an upsert: keep files already on the machine, add what is missing.

Refresh from the live machine: `./scripts/snapshot.sh`. It does not commit.
