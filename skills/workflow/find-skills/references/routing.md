# Catalog routing map

Every skill in this catalog, grouped by the job a user states. Use it with `scripts/catalog.mjs`: the map says what exists, the script says what is installed and how to start it. A chain is the order to run skills. Each skill's own `Related skills` section lists its hand-offs.

Group → plugin: `levistack-<group>`. Group `upstream` means the skill ships as its own plugin from its own repo (see `upstream.json`); the levistack root plugin installs it as a dependency, or install it alone with `claude plugin install <skill>@levistack` or `npx skills add pahlevikun/<skill> -g -y`. A skill in the map but not on disk is installable. Install the group with `claude plugin install levistack-<group>@levistack`, or one skill with `npx skills add pahlevikun/levistack@<skill> -g -y`.

## Understand and decide

| The user wants to… | Chain | Group |
|---|---|---|
| Not sure where to start, or want the full route | `use-levistack` | workflow |
| How one flow or module works, where a change should live | `codebase-learner` (explain mode) | knowledge |
| Why code is shaped this way, what tradeoff or incident caused it | `trace` | knowledge |
| Root cause of a bug, an incident, a flaky or slow pipeline; postmortem; five whys | `verify` (if the failure is live and unexplained), `trace` (root-cause mode) | knowledge |
| Onboard, map a codebase, find architecture smells | `codebase-learner` | knowledge |
| Write docs for a feature, module or API, or check which docs a change made stale | `create-documentation` | delivery |
| Pick a framework, compare X vs Y, cost a migration, plan a greenfield stack | `codebase-learner` (only if facts are missing), `super-tech-blueprint` | architecture |
| Name or choose an architecture style, scaffold in one | `super-architecture` | architecture |
| Grill a plan, stress-test an idea, brainstorm a design | `challenge-me` | knowledge |
| Answer a question from primary sources, the web, or read-only git history on docs and releases, or prepare questions for one person | `research` (sources or people mode) | knowledge |
| Explain a system, schema, API or process with Mermaid, SVG, draw.io or Excalidraw, or export a diagram to an image or animation | `diagram` | product |
| Make a task prompt deeper before running it | `challenge-me` (sharpen mode) | knowledge |
| Plan work too big for one session as a map of decisions | `challenge-me` (decision-map, huge work), then `write-plan` | knowledge |
| Cache design, invalidation, CDN, Redis, offline | `super-caching` | architecture |
| Node.js service, API, middleware, auth | `super-nodejs` | architecture |
| `.proto`, buf, gRPC or Connect, schema breaks | `super-protobuf` | architecture |
| A palette, brand colors, a theme, dark mode, color tokens, a contrast fix, a color audit, a theme for Flutter or Compose or SwiftUI | `color-kit` | product |
| Build or review one screen, a component, an interaction, a gesture, a transition or motion for iOS, Android, React Native, Flutter, desktop, web, car (driving) or TV | `ui-ux-kit` | product |
| A whole design system, token file, DESIGN.md, governance, extract a site's design, critique a UI against a system (calls `color-kit` and `ui-ux-kit`) | `design-system-kit` | product |
| Build a throwaway prototype, a wireframe or a screen map to answer a design or behavior question | `prototype-wireframe` | product |
| Logo, icon, README banner or SVG brand kit | `logo-kit-svg` | upstream |
| Audit or polish a shipped product: code, journeys, branding, motion audit (calls `color-kit`, `ui-ux-kit` and `design-system-kit` for their parts), `verify` | `product-polish-workflow` | product |

## Plan and build

| The user wants to… | Chain | Group |
|---|---|---|
| Plan a multi-step change before code | `challenge-me` (if the spec is soft), `write-plan` | knowledge |
| Slice a big plan into end-to-end pieces with blockers | `write-plan` (slicing), `create-tickets` for tickets | knowledge |
| Spec a backend or API change (lifecycle, errors, compatibility) | `codebase-learner` (if the flow is unknown), `ready-spec`, `write-plan` | knowledge |
| Build a feature or fix a bug test-first | `tdd`, `verify` | engineering |
| Elixir, Phoenix, Ecto, OTP work | `super-elixir` (its tdd speciality for test-first), `verify` | engineering |
| Refactor without changing behavior | `tdd` (if no safety net), `safe-refactor`, `verify` | engineering |
| Write the smallest change, cut over-engineering | `output-savers` (`principles`) | engineering |
| Filter generated code for slop, clean comments | `noslop` (`noslop-code` for comments only) | engineering |

## Verify, review, ship

| The user wants to… | Chain | Group |
|---|---|---|
| Prove work is done, run the gates, find a failure's cause | `verify` | engineering |
| Prove a change is safe, or find what it could break | `verify` (prove it is safe), `second-opinion` for a wide change | engineering |
| Check a performance number before you report it | `verify` (vet a number) | engineering |
| Prune weak or duplicate tests in an existing suite | `tdd` (audit mode) | engineering |
| Adversarial review, blind spots before merge | `second-opinion`, `verify` for each Act on fix | knowledge |
| Review a local diff or a merge request, act on review comments | `glab-code-review` (`noslop` dimension), `verify` for each comment | delivery |
| Split a messy tree into commits | `atomic-semantic-commit` | delivery |
| Open or describe an MR or PR | `atomic-semantic-commit` (if mixed), `glab-code-review` (self-review), `write-mr-description` | delivery |
| Write Jira stories or tasks | `challenge-me` or `write-plan` (if not broken down), `create-tickets` | delivery |
| Build a Bruno API collection | `create-bruno-collection`, then `verify` to run it | delivery |

## Write

| The user wants to… | Chain | Group |
|---|---|---|
| Write or rewrite prose for people: email, chat, docs, comments, incident update | `polyglot-copywriter` | upstream |
| Turn evidence into an editorial infographic, comparison, timeline or visual explanation, including Mermaid or animated figures | `infographic`, with `diagram` for technical source and exports | product |
| Short replies, save tokens, plain technical style for agents | `output-savers` (`concise`; `concise-light` or `concise-heavy` for a level) | engineering |

## Author agent tooling

| The user wants to… | Chain | Group |
|---|---|---|
| Write or fix a skill | `find-skills` (does one exist?), `create-skill` | agent-authoring |
| Learn from a session or repeated mistakes across commits and reviews | `retrospective` (session or repo mode) | agent-authoring |
| Retro an epic, initiative, or sprint; reconstruct what happened on a ticket or PR | `retrospective` (initiative or artifact mode) | agent-authoring |
| Dev machine, container, or CI setup keeps failing the same way | `retrospective` (environment mode) | agent-authoring |
| Turn a rule, command, agent, doc, PDF or chat into a skill; merge skills | `convert-as-skill`, then `create-skill` to polish | agent-authoring |
| Write a subagent | `create-agent` | agent-authoring |
| Write a slash command | `create-command` | agent-authoring |
| Write a rule or coding standard | `create-rule` | agent-authoring |
| Automate on an agent event | `create-hook` | agent-authoring |
| Write or refresh AGENTS.md or CLAUDE.md | `codebase-learner` (if the repo is unknown), `create-agents-md` | agent-authoring |
| Not sure if it is a rule, hook, skill, command or agent | `create-skill` (it has the decision table) | agent-authoring |

## Session and focus

| The user wants to… | Chain | Group |
|---|---|---|
| Stop or resume a session | `handoff` | workflow |
| Catch up on a long chat, or rebuild context when there is no note | `handoff` (catch up or recall mode) | workflow |
| Write today's standup | `standup`, `polyglot-copywriter` for the final polish | focus |
| Overwhelmed, stuck or avoiding a task | `get-moving` | focus |
| A tangent appeared mid-task | `later-list`, then back to the task | focus |
| Do not know which skill to use | `use-levistack` (it calls `find-skills` to hunt) | workflow |
| Find, compare or install a skill | `find-skills` | workflow |

## Worked chains

| User says | Chain |
|---|---|
| "Modify the polyglot-copywriter skill" | It is an upstream skill: edit it in `pahlevikun/polyglot-copywriter`, not here. For a catalog skill in this repo: `manage-stack` (write surface and checks), `create-skill` (authoring rules and lint), edit, lint, `npm run check`. Elsewhere: `create-skill`, edit, lint. |
| "Write an MR for this branch" | `atomic-semantic-commit` if the diff is mixed, `glab-code-review` self-review, `write-mr-description`. |
| "Add an Elixir feature with tests" | `write-plan` if large, `tdd` (Elixir track), `super-elixir` code-review, `verify`. |
| "Which stack should we move to?" | `codebase-learner`, `super-tech-blueprint`, `challenge-me` on the pick, `write-plan`. |
| "Turn this plan into tickets" | `write-plan` if the plan is missing, `create-tickets`. |
| "Ship this fix" | `tdd`, `verify`, `atomic-semantic-commit`, `write-mr-description`. |
