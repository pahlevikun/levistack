# Infographic agent packaging

| File | Use |
|---|---|
| `openai.yaml` | Default display name, short description, and starter prompt for OpenAI-style agent hosts |

In levistack, the shipped skill entry point is `../SKILL.md` (`name: infographic`). Hosts that install only this folder should load that file and the references it links.

Prompt examples live in `../references/prompt-recipes.md`. A worked brief lives in `../examples/cfo-capacity/brief.md`.
