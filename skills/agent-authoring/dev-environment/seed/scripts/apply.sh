#!/usr/bin/env bash
# Re-apply this laptop-setup snapshot on any Mac. Upsert: keep what exists, add what is missing.
# Usage: ./apply.sh [--help]
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${LAPTOP_SETUP_BACKUP:-$HOME/.laptop-setup-backups/$STAMP}"

DO_BREW=1
DO_ZSH=1
DO_DOTFILES=1
DO_KEYS=1
DO_LANGS=1
DO_EXTRAS=1
DO_AGENTS=1
DO_LAUNCH=1
DO_EDITORS=1
DO_CHROME=0
DO_CLONES=0
DRY=0
YES=0

usage() {
  cat <<'EOF'
Re-apply laptop-setup on this Mac. Safe to run more than once.

  ./apply.sh                 upsert brew, zsh, configs, languages, agents, LaunchAgents
                             (keep current files; add missing packages/plugins/keys)
  ./apply.sh --with-clones   also clone git remotes from snapshots/git-repos.tsv
  ./apply.sh --with-chrome   also open Chrome Web Store pages
  ./apply.sh --only brew     run one step
  ./apply.sh --skip-langs    skip the slow language installs
  ./apply.sh --dry-run       print commands only
  ./apply.sh -y              no confirm prompt

Steps: brew zsh dotfiles keys langs extras agents launch editors chrome clones

Secrets are not in git. Put SSH private keys in ./private/ if you have them.
Sign in to CLIs yourself. Do not paste tokens into shell files.
EOF
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
log() { printf '\n==> %s\n' "$*"; }
note() { printf '    %s\n' "$*"; }

run() {
  if [[ "$DRY" -eq 1 ]]; then
    printf 'DRY %s\n' "$*"
    return 0
  fi
  "$@"
}

run_curl_sh() {
  local url="$1"
  shift
  if [[ "$DRY" -eq 1 ]]; then
    printf 'DRY curl %s | sh\n' "$url"
    return 0
  fi
  curl -fsSL "$url" | "$@"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --dry-run) DRY=1 ;;
    -y|--yes) YES=1 ;;
    --skip-brew) DO_BREW=0 ;;
    --skip-zsh) DO_ZSH=0 ;;
    --skip-dotfiles) DO_DOTFILES=0 ;;
    --skip-keys) DO_KEYS=0 ;;
    --skip-langs) DO_LANGS=0 ;;
    --skip-extras) DO_EXTRAS=0 ;;
    --skip-agents) DO_AGENTS=0 ;;
    --skip-launch) DO_LAUNCH=0 ;;
    --skip-editors) DO_EDITORS=0 ;;
    --with-chrome) DO_CHROME=1 ;;
    --with-clones) DO_CLONES=1 ;;
    --only)
      [[ $# -ge 2 ]] || die "--only needs a step name"
      DO_BREW=0; DO_ZSH=0; DO_DOTFILES=0; DO_KEYS=0
      DO_LANGS=0; DO_EXTRAS=0; DO_AGENTS=0; DO_LAUNCH=0
      DO_EDITORS=0; DO_CHROME=0; DO_CLONES=0
      case "$2" in
        brew) DO_BREW=1 ;;
        zsh) DO_ZSH=1 ;;
        dotfiles) DO_DOTFILES=1 ;;
        keys) DO_KEYS=1 ;;
        langs) DO_LANGS=1 ;;
        extras) DO_EXTRAS=1 ;;
        agents) DO_AGENTS=1 ;;
        launch) DO_LAUNCH=1 ;;
        editors) DO_EDITORS=1 ;;
        chrome) DO_CHROME=1 ;;
        clones) DO_CLONES=1 ;;
        *) die "unknown step: $2" ;;
      esac
      shift
      ;;
    *) die "unknown flag: $1 (see --help)" ;;
  esac
  shift
done

ensure_brew_on_path() {
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
}

rewrite_home_placeholder() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  case "$f" in
    *.plist|*.json) ;;
    *) return 0 ;;
  esac
  if grep -q '\$HOME' "$f" 2>/dev/null; then
    if [[ "$DRY" -eq 1 ]]; then
      note "rewrite \$HOME -> $HOME in $f"
      return 0
    fi
    sed -i '' 's|\$HOME|'"$HOME"'|g' "$f"
  fi
}

backup_if_needed() {
  local dest="$1" rel
  [[ -e "$dest" ]] || return 0
  [[ "$DRY" -eq 1 ]] && return 0
  rel="${dest#"$HOME"/}"
  mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
  cp -p "$dest" "$BACKUP_DIR/$rel" 2>/dev/null || true
}

copy_file() {
  local src="$1" dest="$2" mode="${3:-}"
  backup_if_needed "$dest"
  run mkdir -p "$(dirname "$dest")"
  run cp "$src" "$dest"
  rewrite_home_placeholder "$dest"
  if [[ -n "$mode" && "$DRY" -eq 0 ]]; then
    chmod "$mode" "$dest"
  fi
}

# Upsert: keep dest if it exists; add missing JSON keys / zsh plugins; copy only when absent.
upsert_file() {
  local src="$1" dest="$2" mode="${3:-}"
  if [[ ! -e "$dest" ]]; then
    copy_file "$src" "$dest" "$mode"
    return 0
  fi
  case "$dest" in
    *.json)
      note "json upsert $dest"
      if [[ "$DRY" -eq 1 ]]; then
        return 0
      fi
      python3 "$REPO/scripts/upsert.py" json "$src" "$dest"
      rewrite_home_placeholder "$dest"
      ;;
    */.zshrc)
      note "zshrc plugin upsert $dest"
      if [[ "$DRY" -eq 1 ]]; then
        return 0
      fi
      python3 "$REPO/scripts/upsert.py" zshrc-plugins "$src" "$dest"
      ;;
    *)
      note "keep existing $dest"
      ;;
  esac
}

confirm() {
  [[ "$YES" -eq 1 || "$DRY" -eq 1 ]] && return 0
  [[ -t 0 ]] || return 0
  printf 'Apply laptop-setup to %s ? [y/N] ' "$HOME"
  read -r ans
  [[ "$ans" == y || "$ans" == Y ]] || die "aborted"
}

step_preflight() {
  log "preflight"
  [[ "$(uname -s)" == Darwin ]] || die "this snapshot is macOS-only"
  if ! xcode-select -p >/dev/null 2>&1; then
    note "installing Xcode Command Line Tools — re-run this script when it finishes"
    run xcode-select --install || true
    die "wait for CLT, then ./apply.sh again"
  fi
  ensure_brew_on_path
  note "repo=$REPO"
  note "home=$HOME"
  note "backup=$BACKUP_DIR"
}

step_brew() {
  [[ "$DO_BREW" -eq 1 ]] || return 0
  log "homebrew"
  if ! command -v brew >/dev/null 2>&1; then
    note "installing Homebrew"
    run_curl_sh https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh \
      env NONINTERACTIVE=1 /bin/bash
    ensure_brew_on_path
  fi
  command -v brew >/dev/null 2>&1 || die "brew not on PATH after install"
  note "brew bundle (formulae + casks)"
  run brew bundle --file "$REPO/Brewfile"
}

step_zsh() {
  [[ "$DO_ZSH" -eq 1 ]] || return 0
  log "zsh + Oh My Zsh"
  if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
    run_curl_sh https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh \
      env RUNZSH=no CHSH=no KEEP_ZSHRC=yes sh
  fi
  local custom="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins"
  run mkdir -p "$custom"
  while read -r name url; do
    [[ -z "${name:-}" || "$name" == \#* ]] && continue
    if [[ -d "$custom/$name/.git" ]]; then
      note "omz plugin exists: $name"
      continue
    fi
    run git clone --depth 1 "$url" "$custom/$name"
  done < "$REPO/snapshots/omz-plugins.txt"
  local zsh_path
  zsh_path="$(command -v zsh || true)"
  if [[ -n "$zsh_path" && "$SHELL" != "$zsh_path" ]]; then
    if grep -qx "$zsh_path" /etc/shells 2>/dev/null; then
      run chsh -s "$zsh_path" || note "chsh failed; set login shell to zsh manually"
    fi
  fi
}

step_dotfiles() {
  [[ "$DO_DOTFILES" -eq 1 ]] || return 0
  log "dotfiles from home/"
  local src rel dest
  while IFS= read -r -d '' src; do
    rel="${src#"$REPO/home/"}"
    case "$rel" in
      Library/LaunchAgents/sh.atuin.daemon.plist) continue ;;
    esac
    dest="$HOME/$rel"
    upsert_file "$src" "$dest"
  done < <(find "$REPO/home" -type f -print0)
  run mkdir -p "$HOME/.ssh" "$HOME/.vsh" "$HOME/Library/LaunchAgents"
  if [[ "$DRY" -eq 0 ]]; then
    chmod 700 "$HOME/.ssh" 2>/dev/null || true
    chmod 600 "$HOME/.ssh/config" "$HOME/.ssh/known_hosts" 2>/dev/null || true
    chmod 644 "$HOME/.ssh/"*.pub 2>/dev/null || true
  fi
}

step_keys() {
  [[ "$DO_KEYS" -eq 1 ]] || return 0
  log "ssh keys"
  run mkdir -p "$HOME/.ssh"
  if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
    note "keep existing SSH key"
  elif [[ -f "$REPO/private/.ssh/id_ed25519" ]]; then
    copy_file "$REPO/private/.ssh/id_ed25519" "$HOME/.ssh/id_ed25519" 600
  fi
  if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
    run ssh-add --apple-use-keychain "$HOME/.ssh/id_ed25519" || true
  fi
}

step_langs() {
  [[ "$DO_LANGS" -eq 1 ]] || return 0
  log "language versions"
  ensure_brew_on_path
  export PATH="${HOME}/.jenv/bin:${HOME}/.goenv/bin:${HOME}/.rbenv/bin:${PATH}"
  export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:${PATH}"
  export GOENV_ROOT="${GOENV_ROOT:-$HOME/.goenv}"

  local ruby_ver go_ver java_ver fvm_chan plugin prefix jdk
  ruby_ver="$(tr -d '[:space:]' < "$REPO/home/.rbenv/version")"
  go_ver="$(tr -d '[:space:]' < "$REPO/home/.goenv/version")"
  java_ver="$(tr -d '[:space:]' < "$REPO/home/.jenv/version")"
  fvm_chan="$(tr -d '[:space:]' < "$REPO/home/.fvm/default")"

  if command -v rbenv >/dev/null 2>&1; then
    note "rbenv $ruby_ver"
    if [[ "$DRY" -eq 0 ]]; then
      eval "$(rbenv init - bash)" || true
      rbenv install -s "$ruby_ver"
      rbenv global "$ruby_ver"
    fi
  fi

  if command -v goenv >/dev/null 2>&1; then
    note "goenv $go_ver"
    if [[ "$DRY" -eq 0 ]]; then
      eval "$(goenv init -)" || true
      goenv install -s "$go_ver"
      goenv global "$go_ver"
    fi
  fi

  if command -v jenv >/dev/null 2>&1; then
    note "jenv $java_ver"
    if [[ "$DRY" -eq 0 ]]; then
      eval "$(jenv init -)" || true
      jenv enable-plugin export || true
      for jdk in 11 17 21 25; do
        prefix="$(brew --prefix "openjdk@$jdk" 2>/dev/null || true)"
        if [[ -n "$prefix" && -d "$prefix/libexec/openjdk.jdk/Contents/Home" ]]; then
          jenv add "$prefix/libexec/openjdk.jdk/Contents/Home" || true
        fi
      done
      jenv global "$java_ver" || jenv global 21 || true
    fi
  fi

  if command -v asdf >/dev/null 2>&1; then
    while read -r plugin; do
      [[ -z "${plugin:-}" || "$plugin" == \#* ]] && continue
      if asdf plugin list 2>/dev/null | grep -qx "$plugin"; then
        note "asdf plugin exists: $plugin"
      else
        run asdf plugin add "$plugin" || true
      fi
    done < "$REPO/home/.tool-versions.plugins"
    upsert_file "$REPO/home/.tool-versions" "$HOME/.tool-versions"
    if [[ "$DRY" -eq 0 ]]; then
      (cd "$HOME" && asdf install) || true
    fi
  fi

  if command -v fvm >/dev/null 2>&1; then
    note "fvm $fvm_chan"
    run fvm install "$fvm_chan"
    run fvm global "$fvm_chan"
  fi
}

step_extras() {
  [[ "$DO_EXTRAS" -eq 1 ]] || return 0
  log "uv / bun / atuin / optional CLIs"
  ensure_brew_on_path
  export PATH="$HOME/.local/bin:$HOME/.atuin/bin:$HOME/.bun/bin:$PATH"

  if ! command -v uv >/dev/null 2>&1; then
    run_curl_sh https://astral.sh/uv/install.sh sh
  fi
  if ! command -v bun >/dev/null 2>&1; then
    run_curl_sh https://bun.sh/install bash
  fi
  if ! command -v atuin >/dev/null 2>&1; then
    if [[ "$DRY" -eq 1 ]]; then
      note "would install atuin"
    else
      curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
    fi
  fi
  if ! command -v claude >/dev/null 2>&1; then
    run_curl_sh https://claude.ai/install.sh bash || note "claude CLI install failed; install later"
  fi
  if command -v npm >/dev/null 2>&1; then
    command -v claude-mem >/dev/null 2>&1 || run npm install -g claude-mem || true
    command -v copilot >/dev/null 2>&1 || run npm install -g @github/copilot || true
  fi
}

step_agents() {
  [[ "$DO_AGENTS" -eq 1 ]] || return 0
  log "agent config + skill symlinks"
  run mkdir -p "$HOME/Documents/example-project" "$HOME/.cursor/plugins/local" \
    "$HOME/.cursor" "$HOME/.claude" "$HOME/.codex"

  if [[ -d "$HOME/.agents/.git" ]]; then
    note "$HOME/.agents already present"
  else
    note "$HOME/.agents is missing; clone it yourself before the skill symlinks"
  fi

  if [[ -d "$HOME/.agents/skills" ]]; then
    run ln -sfn "$HOME/.agents/skills" "$HOME/.cursor/skills"
    run ln -sfn "$HOME/.agents/skills" "$HOME/.claude/skills"
    run ln -sfn "$HOME/.agents/skills" "$HOME/.codex/skills"
  fi
  if [[ -f "$REPO/home/.agents/mcp/servers.json" ]]; then
    run mkdir -p "$HOME/.agents/mcp"
    upsert_file "$REPO/home/.agents/mcp/servers.json" "$HOME/.agents/mcp/servers.json"
    run ln -sfn "$HOME/.agents/mcp/servers.json" "$HOME/.cursor/mcp.json"
  fi

  if [[ -x "$HOME/.agents/bin/aicfg" ]]; then
    run "$HOME/.agents/bin/aicfg" update || true
  fi
}

write_plist() {
  local dest="$1"
  backup_if_needed "$dest"
  if [[ "$DRY" -eq 1 ]]; then
    note "write $dest"
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  cat > "$dest"
}

bootstrap_launch() {
  local label="$1" plist="$2"
  [[ -f "$plist" ]] || return 0
  local uid
  uid="$(id -u)"
  if launchctl print "gui/${uid}/${label}" >/dev/null 2>&1; then
    note "keep running $label"
    return 0
  fi
  run launchctl bootstrap "gui/${uid}" "$plist" || true
}

step_launch() {
  [[ "$DO_LAUNCH" -eq 1 ]] || return 0
  log "LaunchAgents"
  run mkdir -p "$HOME/.claude-mem/logs" "$HOME/.ia-mcp/logs" "$HOME/.atuin/logs" \
    "$HOME/Library/LaunchAgents"

  local src dest
  for src in "$REPO/home/Library/LaunchAgents/"*.plist; do
    [[ -f "$src" ]] || continue
    local base
    base="$(basename "$src")"
    [[ "$base" == sh.atuin.daemon.plist ]] && continue
    dest="$HOME/Library/LaunchAgents/$base"
    upsert_file "$src" "$dest" 644
  done

  if [[ -f "$HOME/Library/LaunchAgents/sh.atuin.daemon.plist" ]]; then
    note "keep existing Atuin LaunchAgent"
  elif command -v atuin >/dev/null 2>&1 || [[ -x "$HOME/.atuin/bin/atuin" ]]; then
    local atuin_bin="${HOME}/.atuin/bin/atuin"
    command -v atuin >/dev/null 2>&1 && atuin_bin="$(command -v atuin)"
    write_plist "$HOME/Library/LaunchAgents/sh.atuin.daemon.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>sh.atuin.daemon</string>
  <key>ProgramArguments</key>
  <array>
    <string>${atuin_bin}</string>
    <string>daemon</string>
    <string>start</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key>
  <dict><key>Crashed</key><true/></dict>
  <key>WorkingDirectory</key><string>${HOME}/.atuin</string>
  <key>StandardErrorPath</key><string>${HOME}/.atuin/logs/daemon.stderr.log</string>
</dict>
</plist>
EOF
  fi

  bootstrap_launch ai.claude-mem.worker "$HOME/Library/LaunchAgents/ai.claude-mem.worker.plist"
  if [[ -d "$HOME/.agents/ia-mcp" ]]; then
    bootstrap_launch ai.ia-mcp.web "$HOME/Library/LaunchAgents/ai.ia-mcp.web.plist"
  else
    note "skip ia-mcp LaunchAgent (clone ~/.agents first)"
  fi
  bootstrap_launch sh.atuin.daemon "$HOME/Library/LaunchAgents/sh.atuin.daemon.plist"
}

step_editors() {
  [[ "$DO_EDITORS" -eq 1 ]] || return 0
  log "Cursor / VS Code extensions"
  if [[ "$DRY" -eq 1 ]]; then
    note "would run scripts/install-editor-extensions.sh"
    return 0
  fi
  "$REPO/scripts/install-editor-extensions.sh" || true
}

step_chrome() {
  [[ "$DO_CHROME" -eq 1 ]] || return 0
  log "Chrome extensions (opens Web Store tabs)"
  if [[ "$DRY" -eq 1 ]]; then
    note "would run scripts/install-chrome-extensions.sh"
    return 0
  fi
  "$REPO/scripts/install-chrome-extensions.sh" || true
}

step_clones() {
  [[ "$DO_CLONES" -eq 1 ]] || return 0
  log "git remotes (181)"
  if [[ "$DRY" -eq 1 ]]; then
    note "would run scripts/clone-repos.sh"
    return 0
  fi
  "$REPO/scripts/clone-repos.sh"
}

step_report() {
  log "done"
  cat <<EOF
Upserted from $REPO onto $HOME (existing files kept; missing ones added)
Backups of first-time copies: $BACKUP_DIR

Still manual:
  1. Sign in to CLIs that need a token. Do not paste the value into a shell file.
  2. Do not start Colima unless you want Docker running.

Optional later:
  ./apply.sh --with-clones
  ./apply.sh --with-chrome
EOF
}

confirm
step_preflight
step_brew
step_zsh
step_dotfiles
step_keys
step_langs
step_extras
step_agents
step_launch
step_editors
step_chrome
step_clones
step_report
