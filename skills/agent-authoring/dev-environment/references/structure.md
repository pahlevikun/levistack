# Directory structure

Create this layout on first run. Empty clone slots come from `seed/structure/home-dirs.txt` (`mkdir -p`, never delete).

## Skill (`dev-environment/`)

```text
dev-environment/
├── SKILL.md
├── references/
│   └── structure.md          ← this file
├── scripts/
│   ├── init-repo.sh          # materialize snapshot repo + $HOME dirs
│   ├── apply                 # init-repo, then dest ./apply.sh
│   └── snapshot              # init-repo, then dest scripts/snapshot.sh
└── seed/                     # copy of the snapshot repo (no .git, no private keys)
    ├── apply.sh
    ├── Brewfile
    ├── README.md
    ├── SETUP.md
    ├── .gitignore
    ├── home/                 # files to upsert into $HOME
    ├── scripts/
    ├── snapshots/
    └── structure/
        └── home-dirs.txt     # every $HOME directory to mkdir
```

## Snapshot repo (`$LAPTOP_SETUP_ROOT`, default `$HOME/laptop-setup`)

```text
laptop-setup/
├── apply.sh
├── Brewfile
├── README.md
├── SETUP.md
├── .gitignore
├── home/
│   ├── .zshrc
│   ├── .gitconfig
│   ├── .ssh/                 # config, *.pub, known_hosts (no private keys)
│   ├── .vsh/                 # config.yaml + vsh_id.pub
│   ├── .oh-my-zsh/custom/    # legacy-shortcuts.zsh, dev-aliases.zsh
│   ├── .agents/mcp/servers.json
│   ├── .atuin/
│   ├── .tsh/
│   ├── .config/gcloud/
│   └── Library/LaunchAgents/
├── scripts/
│   ├── apply.sh
│   ├── snapshot.sh
│   ├── upsert.py
│   ├── clone-repos.sh
│   ├── install-editor-extensions.sh
│   └── install-chrome-extensions.sh
└── snapshots/
    ├── git-repos.tsv         # origin URLs only
    ├── git-repos.md
    ├── omz-plugins.txt
    ├── vscode-extensions.txt
    ├── chrome-extensions.tsv
    ├── applications.txt
    ├── asdf-plugins.txt
    ├── brew-list.txt
    ├── languages.txt
    ├── claude-plugins.txt
    ├── codex-plugins.txt
    ├── cursor-agents.txt
    ├── cursor-plugins-local.txt
    ├── layout.txt
    ├── npm-global.txt
    ├── private-files.md
    ├── skills.txt
    ├── versions.txt
    └── vsh.txt
```

`seed/home/` also holds `settings.json` and LaunchAgent plists `ai.claude-mem.worker.plist`, `ai.ia-mcp.web.plist`, and `sh.atuin.daemon.plist`.

`private/` is gitignored and is **not** in the seed. Put SSH/vsh private keys there by hand.

## Live `$HOME` (created by init-repo)

Top-level:

```text
~/
├── .zshrc
├── .oh-my-zsh/custom/{plugins,themes}
├── .ssh/
├── .vsh/
├── .agents/                  # clone agentic-tools here
│   ├── skills/               # Cursor/Claude/Codex dir-symlink here
│   └── mcp/
├── .cursor/plugins/{local,cache}
├── .atuin/
├── .local/bin/
├── Library/LaunchAgents/
└── Documents/
    └── example-project/
```

Every clone destination listed in `snapshots/git-repos.tsv` is also created as an empty directory (see `seed/structure/home-dirs.txt`). `scripts/clone-repos.sh` fills those dirs. Do not add convenience symlinks.
