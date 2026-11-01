# Everyday CLI aliases. OMZ git plugin already provides gst/gco/gd/gl/gp.

# eza instead of ls
if command -v eza >/dev/null; then
  alias ls='eza --group-directories-first'
  alias ll='eza -l --group-directories-first --git'
  alias la='eza -la --group-directories-first --git'
  alias lt='eza -T --level=2 --group-directories-first'
  alias l='ll'
fi

# bat instead of cat for highlighting
if command -v bat >/dev/null; then
  alias cat='bat --paging=never --style=plain'
  alias preview='bat'
fi

# zoxide
command -v zoxide >/dev/null && alias j='z'

# git
alias lg='lazygit'

# k8s
alias k='kubectl'
alias kx='kubectx'
alias kn='kubens'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'

# docker / colima
alias dc='docker compose'
alias dps='docker ps'
alias colima-start='colima start'
alias colima-stop='colima stop'

# claude-mem viewer
alias cm-ui='open http://127.0.0.1:37777'

# ia-mcp dashboard (pairs with claude-mem on :37777)
alias ia-ui='open http://127.0.0.1:37778'
alias ia-status='uv run --project "$HOME/.agents/ia-mcp" python -m src.cli status'
alias ia-web='uv run --project "$HOME/.agents/ia-mcp" python -m src.cli web'

# history-substring-search arrows
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
bindkey '^P' history-substring-search-up
bindkey '^N' history-substring-search-down
