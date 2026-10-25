# Plugin and extension architecture

A stable host that other code extends without changing the host. This guide gives the host-extension principles and the concrete shape of a Claude Code plugin. For a general platform (IDE, marketplace, sandboxed third-party code, compatibility matrix), use `styles/microkernel/GUIDE.md`.

## Pick when
- Third parties or other teams must add capabilities to a core.
- You ship a bundle of related capabilities (commands, agents, skills, hooks) to be installed together.
- Optional features should be enabled, disabled and versioned independently.

## Avoid when
- A closed application with one team and no extension need. Plain modules are simpler.

## Principles
1. **A small, stable host API.** Extensions depend on it; it changes rarely and with versioning.
2. **Convention-based discovery.** Extensions are found by location and naming, not by editing the host.
3. **Isolation.** A broken extension must not take down the host; load failures are reported, not fatal.
4. **Portable paths.** Extensions refer to their own files through a host-provided root variable, never absolute paths.
5. **Declarative manifest.** Name, version, description and component locations in one file.
6. **Per-project settings are separate from code,** kept in a file that is not committed when it holds personal state.
7. **Semantic versioning,** and a compatibility statement against the host.

## Claude Code plugin structure

```
my-plugin/
  .claude-plugin/
    plugin.json        manifest (the only thing inside this folder)
  commands/            slash commands, one .md file each
  agents/              subagents, one .md file each
  skills/              one subfolder per skill, each with SKILL.md
  hooks/hooks.json     hook configuration
  .mcp.json            MCP servers
  scripts/             helper scripts used by hooks and commands
```

Rules:
- The manifest lives in `.claude-plugin/plugin.json`; component folders sit at the plugin **root**, not inside `.claude-plugin/`.
- Create folders only for components you use.
- Use kebab-case for folder and file names; the plugin name is unique across installed plugins.
- `plugin.json` requires `name`; add `version` (semantic), `description`, `author`, `keywords`.
- Custom component paths in the manifest **supplement** the default folders (they do not replace them), must be relative and start with `./`, and may be arrays.
- Reference files inside the plugin with the `${CLAUDE_PLUGIN_ROOT}` variable in hooks, MCP configs and scripts, never with hardcoded paths.
- Discovery: the host reads the manifest when the plugin is enabled, scans `commands/` and `agents/` for markdown files and `skills/` for folders containing `SKILL.md`, and loads hooks and MCP configuration. Changes take effect on a new session.

## Plugin settings pattern

Store user-configurable state in `.claude/<plugin-name>.local.md`: YAML frontmatter for settings, the markdown body for free-form notes or prompts. Hooks and commands read the file, parse the frontmatter, and exit quietly when the file is absent.

- Provide defaults when the file does not exist, and validate values you read.
- Add the file to `.gitignore`; it holds per-project or personal state.
- Sanitize any user input written into it and validate file paths it contains.
- Settings changes need a new session to take effect.
- Use it to switch hooks on and off, hold agent state, or drive configuration-dependent behavior.

## Build steps
1. Decide the components and group them logically (one plugin per cohesive capability).
2. Create the manifest and the component folders.
3. Write components with portable paths.
4. Add a settings file pattern if behavior is configurable.
5. Validate the manifest and install locally; confirm each component loads.
6. Version and document how to enable it.

## Pitfalls
Manifest in the wrong folder, components nested inside `.claude-plugin/`, hardcoded paths, forgetting that custom paths add rather than replace, committing a local settings file, a plugin that bundles unrelated capabilities.

## Combines with
Microkernel (the general platform: sandbox, SDK, compatibility matrix), hexagonal (the host exposes ports, extensions are adapters), event-driven (extensions react to host events).
