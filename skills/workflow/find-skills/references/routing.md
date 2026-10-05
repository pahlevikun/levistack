# Catalog routing map

Every skill in this catalog, grouped by the job a user states. Use it with `scripts/catalog.mjs`: the map says what exists, the script says what is installed and how to start it. A chain is the order to run skills. Each skill's own `Related skills` section lists its hand-offs.

Group → plugin: `levistack-<group>`. A skill in the map but not on disk is installable. Install the group with `claude plugin install levistack-<group>@levistack`, or one skill with `npx skills add pahlevikun/levistack@<skill> -g -y`.

## Understand and decide

| The user wants to… | Chain | Group |
|---|---|---|
| Onboard, map a codebase, find architecture smells | `super-codebase-learner` | knowledge |
| Pick a framework, compare X vs Y, cost a migration, plan a greenfield stack | `super-codebase-learner` (only if facts are missing), `super-tech-blueprint` | architecture |
| Name or choose an architecture style, scaffold in one | `super-architecture` | architecture |
| Grill a plan, stress-test an idea, brainstorm a design | `super-challenge-me` | knowledge |
| Cache design, invalidation, CDN, Redis, offline | `super-caching` | architecture |
| Node.js service, API, middleware, auth | `super-nodejs` | architecture |
| `.proto`, buf, gRPC or Connect, schema breaks | `super-protobuf` | architecture |
| UI critique, design tokens, component specs, accessibility | `super-design` | engineering |

## Plan and build

| The user wants to… | Chain | Group |
|---|---|---|
| Plan a multi-step change before code | `super-challenge-me` (if the spec is soft), `writing-plans` | knowledge |
| Build a feature or fix a bug test-first | `super-tdd`, `super-verify` | engineering |
| Elixir, Phoenix, Ecto, OTP work | `super-elixir` (its tdd speciality for test-first), `super-verify` | engineering |
| Refactor without changing behavior | `super-tdd` (if no safety net), `super-refactor`, `super-verify` | engineering |
| Write the smallest change, cut over-engineering | `output-savers` (`principles`) | engineering |
| Filter generated code for slop, clean comments | `super-noslop` (`super-noslop-code` for comments only) | engineering |

## Verify, review, ship

| The user wants to… | Chain | Group |
|---|---|---|
| Prove work is done, run the gates, find a failure's cause | `super-verify` | engineering |
| Review a local diff or a merge request, act on review comments | `glab-code-review` (`super-noslop` dimension), `super-verify` for each comment | delivery |
| Split a messy tree into commits | `atomic-semantic-commit` | delivery |
| Open or describe an MR or PR | `atomic-semantic-commit` (if mixed), `glab-code-review` (self-review), `write-mr-description` | delivery |
| Write Jira stories or tasks | `super-challenge-me` or `writing-plans` (if not broken down), `create-jira-story` | delivery |
| Build a Bruno API collection | `create-bruno-collection`, then `super-verify` to run it | delivery |

## Write

| The user wants to… | Chain | Group |
|---|---|---|
| Write or rewrite prose for people: email, chat, docs, comments, incident update | `polyglot-copywriter` | engineering |
| Short replies, save tokens, plain technical style for agents | `output-savers` (`concise`; `concise-light` or `concise-heavy` for a level) | engineering |

## Author agent tooling

| The user wants to… | Chain | Group |
|---|---|---|
| Write or fix a skill | `find-skills` (does one exist?), `create-skill` | agent-authoring |
| Turn a rule, command, agent, doc, PDF or chat into a skill; merge skills | `convert-as-skill`, then `create-skill` to polish | agent-authoring |
| Write a subagent | `create-agent` | agent-authoring |
| Write a slash command | `create-command` | agent-authoring |
| Write a rule or coding standard | `create-rule` | agent-authoring |
| Automate on an agent event | `create-hook` | agent-authoring |
| Write or refresh AGENTS.md or CLAUDE.md | `super-codebase-learner` (if the repo is unknown), `create-agents-md` | agent-authoring |
| Not sure if it is a rule, hook, skill, command or agent | `create-skill` (it has the decision table) | agent-authoring |

## Session and focus

| The user wants to… | Chain | Group |
|---|---|---|
| Stop or resume a session | `handoff` | workflow |
| Write today's standup | `standup`, `polyglot-copywriter` for the final polish | workflow |
| Overwhelmed or stuck | `one-next-action` | focus |
| A tangent appeared mid-task | `parking-lot`, then back to the task | focus |
| Do not know which skill to use | `find-skills` | workflow |

## Worked chains

| User says | Chain |
|---|---|
| "Modify the polyglot-copywriter skill" | Read that skill's `SKILL.md`. In this repo: `manage-stack` (write surface and checks), `create-skill` (authoring rules and lint), edit, lint, `npm run check`. Elsewhere: `create-skill`, edit, lint. |
| "Write an MR for this branch" | `atomic-semantic-commit` if the diff is mixed, `glab-code-review` self-review, `write-mr-description`. |
| "Add an Elixir feature with tests" | `writing-plans` if large, `super-tdd` (Elixir track), `super-elixir` code-review, `super-verify`. |
| "Which stack should we move to?" | `super-codebase-learner`, `super-tech-blueprint`, `super-challenge-me` on the pick, `writing-plans`. |
| "Turn this plan into tickets" | `writing-plans` if the plan is missing, `create-jira-story`. |
| "Ship this fix" | `super-tdd`, `super-verify`, `atomic-semantic-commit`, `write-mr-description`. |
