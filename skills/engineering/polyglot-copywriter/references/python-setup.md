# Python setup (for the helper scripts)

The scripts in `scripts/` use only the Python standard library. They need Python 3.10 or later. They need no pip packages, no virtual environment, and no requirements file.

## Do you need Python at all?

Only the helper scripts need it:

| Script | Job |
|---|---|
| `find_language.py` | Look up a language, alias, or region |
| `new_language.py`, `new_usecase.py`, `bulk_expand.py` | Scaffold a pack and update the indexes |
| `validate_skill.py`, `evaluate_output.py` | Check the skill and score a case |

Writing, rewriting, and review do not need Python. Never block a writing task on it.

## Step 1: check

```bash
python3 --version     # macOS and Linux
py -3 --version       # Windows (or: python --version)
```

You need 3.10 or later. If the command is missing, or the version is older, go to step 2. Use the command name that worked in every later command.

## Step 2: ask, then install

Installing software changes the user's machine. Ask once before you install, unless the user already asked you to set it up. Do not use `sudo` without the user's approval. Pick the line for the system:

| System | Command |
|---|---|
| macOS with Homebrew | `brew install python` |
| macOS without Homebrew | Install Homebrew from brew.sh, then `brew install python`. Or download the installer from python.org. |
| Ubuntu or Debian | `sudo apt-get update && sudo apt-get install -y python3` |
| Fedora or RHEL | `sudo dnf install -y python3` |
| Arch | `sudo pacman -S --needed python` |
| openSUSE | `sudo zypper install python3` |
| Alpine (container, runs as root) | `apk add python3` |
| Windows with winget | `winget install -e --id Python.Python.3.12` |
| Windows with Chocolatey | `choco install python` |
| Any system with uv | `uv python install 3.12`, then run scripts as `uv run --no-project python scripts/validate_skill.py` |

Notes:

- **Old distributions.** If the package manager gives a Python older than 3.10 (Ubuntu 20.04 has 3.8), use the uv line instead.
- **Windows.** Open a new terminal after the install so the PATH updates. Use `py -3` if `python3` is not found.
- **macOS.** `xcode-select --install` installs Apple's Python. It may be older than 3.10, so check the version.

## Step 3: verify

```bash
python3 --version
python3 scripts/validate_skill.py
```

The first command shows 3.10 or later. The second prints `Validation passed`.

## If you cannot install it

Continue without the scripts:

- **Lookup.** Read `references/registry.json` and search the `id`, `name`, and `aliases` fields.
- **Checks.** Skip `validate_skill.py` and `evaluate_output.py`. Tell the user once that the checks were skipped.
- **Scaffolding.** Copy the template folders under `references/_template/` by hand, and add one row to `references/registry.json`.
