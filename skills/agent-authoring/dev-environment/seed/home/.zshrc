# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# User-local tools first (claude-mem, codegraph, uv, pipx)
export PATH="$HOME/.local/bin:$PATH"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="robbyrussell"

# Extra completions from zsh-completions (must be on fpath before omz loads)
fpath+=${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-completions/src

# zsh-syntax-highlighting must be last-but-one; history-substring-search after it
plugins=(
  git
  brew
  macos
  extract
  sudo
  colored-man-pages
  copypath
  copyfile
  dirhistory
  last-working-dir
  jsontools
  vscode
  docker
  kubectl
  golang
  ruby
  fzf
  direnv
  aliases
  you-should-use
  zsh-completions
  zsh-autosuggestions
  zsh-syntax-highlighting
  history-substring-search
)

source $ZSH/oh-my-zsh.sh

# rbenv (Ruby)
eval "$(rbenv init - zsh)"

# jenv (Java)
export PATH="$HOME/.jenv/bin:$PATH"
eval "$(jenv init -)"

# goenv (Go)
export GOENV_ROOT="$HOME/.goenv"
eval "$(goenv init -)"
export PATH="$GOROOT/bin:$PATH"
export PATH="$PATH:$GOPATH/bin"

# asdf (Node, Python, Rust, …)
export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"

# FVM (Flutter)
export PATH="$HOME/fvm/default/bin:$PATH"
export PATH="$PATH:$HOME/.pub-cache/bin"

# Keg-only Homebrew clients
[[ -d /opt/homebrew/opt/mysql-client/bin ]] && export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
[[ -d /opt/homebrew/opt/libpq/bin ]] && export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
[[ -d /opt/homebrew/opt/curl/bin ]] && export PATH="/opt/homebrew/opt/curl/bin:$PATH"

# Google Cloud SDK (cask or legacy install)
for _gcsdk in /opt/homebrew/share/google-cloud-sdk "$HOME/google-cloud-sdk"; do
  [[ -f "$_gcsdk/path.zsh.inc" ]] && . "$_gcsdk/path.zsh.inc"
  [[ -f "$_gcsdk/completion.zsh.inc" ]] && . "$_gcsdk/completion.zsh.inc"
done
unset _gcsdk

# fzf: OMZ plugin already loaded Ctrl-T (files) and Alt-C (cd).
# Atuin must init AFTER fzf so Ctrl-R stays Atuin history, not fzf.
[[ -f "$HOME/.atuin/bin/env" ]] && . "$HOME/.atuin/bin/env"
command -v atuin >/dev/null && eval "$(atuin init zsh)"

# zoxide (smarter cd: z, zi)
command -v zoxide >/dev/null && eval "$(zoxide init zsh)"

# uv
[[ -f "$HOME/.local/bin/env" ]] && . "$HOME/.local/bin/env"

# bun completions
[[ -s "$HOME/.bun/_bun" ]] && source "$HOME/.bun/_bun"

# Local CLIs if present
[[ -d "$HOME/.agents/bin" ]] && export PATH="$HOME/.agents/bin:$PATH"
[[ -d "$HOME/.local/bin" ]] && export PATH="$HOME/.local/bin:$PATH"

# Shortcuts restored from previous laptop
source "$ZSH/custom/legacy-shortcuts.zsh"

export EDITOR="nvim"
export VISUAL="nvim"
export PAGER="less"
export USE_GKE_GCLOUD_AUTH_PLUGIN=True
