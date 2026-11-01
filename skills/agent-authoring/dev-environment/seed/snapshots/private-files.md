# Secrets that stay off git

| Secret | Where it lives |
|---|---|
| SSH private key | `private/` or the live `~/.ssh` (not this seed) |
| API tokens | environment variables, never a committed file |
| App secrets | the OS keychain |
| Cloud CLI sessions | the live home directory, not this seed |
