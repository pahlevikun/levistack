---
name: super-nodejs
description: "Use for any Node.js backend work: package.json, Express, Fastify, middleware, REST or GraphQL APIs, authentication, database integration, error handling, async patterns, Node security and testing. One skill with two specialities: decide (framework, runtime, architecture, anti-patterns) and build (production-ready service patterns with worked examples). It detects the job and loads only the guide it needs."
when_to_use: "Use proactively when the user asks to build, structure, review or harden a Node.js server or API; asks 'Express or Fastify', 'how should I structure this service', 'where does auth go', 'how do I handle errors or async here'; or is working in a Node project with a server entry point."
metadata:
  version: "1.0.0"
---

# Super Node.js

One skill, two specialities. Call it once. It picks the speciality from the job and loads only that guide.

The guides are kept whole. Each is a full, separate skill that was merged in.

## Step 0: detect the job

Do this first and do not announce it. Read `package.json` (dependencies, `type`, scripts) and the server entry point if the project exists; the facts decide framework-specific advice.

| If the user is doing this | Speciality | Load |
|---|---|---|
| Choosing a framework or runtime, "how should I structure this", reviewing a design, naming an anti-pattern, a decision checklist | best-practices | [best-practices](specialities/best-practices/GUIDE.md) |
| Writing the service: Express or Fastify setup, middleware, auth, database integration, validation, error handling, API design, tests | backend-patterns | [backend-patterns](specialities/backend-patterns/GUIDE.md) |
| A new service from scratch | both, in order | best-practices, then backend-patterns |
| Reviewing existing Node code | best-practices for the principles, backend-patterns for the target shape | both, as needed |

Order of precedence: a security finding, then the user's explicit words, then the detected job. A security issue or data-loss risk is always stated in full sentences.

## Build pipeline: one service, in order

1. **Decide.** [best-practices](specialities/best-practices/GUIDE.md): framework, runtime, layering, what to avoid. Write the decisions down in two or three lines before coding.
2. **Build.** [backend-patterns](specialities/backend-patterns/GUIDE.md): the structure, middleware, auth, data access and error handling that the decisions call for. Open its `references/` only for the topic at hand.
3. **Test.** The testing section of each guide. Run the project's own test command, not a guessed one.
4. **Gate.** Run what `package.json` defines (lint, type check, test). Report any gate you could not run.

## Rules that hold across both guides

1. **Follow the project first.** Match the framework, module system and conventions already in `package.json` and the code; the guides are defaults, not a rewrite order.
2. **One place for each concern.** Validation, authentication and error mapping each live in one layer, not scattered through handlers.
3. **Fail loudly at startup, safely at runtime.** Missing config stops boot; request errors return a controlled response and are logged once.
4. **Never block the event loop.** Anything CPU-heavy or synchronous on a request path is moved off it.

## Related skills

- `super-architecture`: plan the service structure.
- `super-caching`: add a cache.
- `super-protobuf`: add gRPC or Connect.
- `super-tdd`: write a handler test first.

## Done when

- The guide that matches the job was opened, and only that one (plus the second when the job needs it).
- Advice matches the project's actual framework and module system.
- The project's own gates ran, or the ones that did not are named.
