# Domain-driven design

Model the business in the language the business already speaks. DDD answers what the concepts are and what they are called. It does not pick a folder layout: pair it with layered, hexagonal, onion, clean or a modular monolith.

## Pick when
- Domain experts can argue about rules, and the team can talk to the people who do the work.
- The same word means different things in different parts of the business (draw a context boundary).
- The system will grow into complexity you cannot yet name, and you need a language that will survive that growth.

## Avoid when
- CRUD over a form: the model would just be the schema under a new name.
- Single-actor tools with no shared business vocabulary.
- You wanted Clean Architecture, mandatory DTOs or a mapper between every tier. Those are separate choices (`styles/hexagonal/GUIDE.md`, `styles/clean/GUIDE.md`).

## Core idea

**Strategic design is the work.** Discover subdomains, draw bounded contexts, write the ubiquitous language. Entities, value objects and aggregates are how a model reaches code once it exists; they are optional machinery, not the goal. Tactical rules: `core/domain-modeling.md`.

The measure of a model is whether a person in the business recognizes their own job in it.

## Build for now

Once a context exists, one data object passed from the store through the business layer (and, at the start, out to the view) is a legitimate starting state. It is not debt. Split only when shapes actually diverge.

### Divergence protocol

**Trigger:** the view or API contract must stay still while the domain model needs to change.

**Move:** the old object becomes the outward DTO; the new domain object gains a translation. Where fields differ, map them. That is the whole mechanism.

Do not add a DTO, mapper, command type or extra layer "because DDD." Name the need in the change that adds it. A mapper whose fields are all 1:1 copies has no job.

### Shared-type options (cheapest first)

1. Same type in every layer, while shapes match.
2. Builder, when contexts select different subsets of one field set.
3. Shared base with per-context subclasses, only when duplication is the larger present pain. Inheritance couples every consumer of the base; treat it as a leak risk at IO boundaries.

### IO boundary (non-negotiable)

Do not reuse a type across a network or other IO boundary without auditing what it exposes. A field added to a shared base appears in every serialized form that inherits it. When two systems exchange commands and do not deploy atomically, a versioned request DTO is a deployment constraint, not a DDD principle; say so in the ADR.

## Strangle an existing app into domains

Never all layers in one pass. Per domain, in order:

1. Data: split fetching to a reasonable domain boundary.
2. Business: one entity (or module) responsible for that domain.
3. Redirect existing call sites onto it.
4. View or API last.

Then the next domain. Keep the implementation simple until a named need appears.

## Build steps
1. Talk to the people who do the work. Write a glossary they would sign.
2. Draw bounded contexts: a term that means two things is two contexts. Map relationships (customer/supplier, conformist, anticorruption layer, shared kernel).
3. Create the store and one object; pass it through.
4. Wait for divergence; apply the protocol.
5. Audit every type that crosses IO.
6. Apply tactical patterns only where invariants need them (`core/domain-modeling.md`).

## Testing
- Domain tests use business words in the names (`cancels an unpaid order`, not `updateStatus`).
- Characterization tests around a slice before strangling it.
- No test should require a DTO that production does not yet need.

## Pitfalls
Ceremony without need. Anemic models (rules live only in services). Silent field leaks across IO. Treating DDD as a folder template. Inventing ubiquitous language the business does not use.

## Combines with
Any in-process structure; modular monolith (one module per context); microservices (one service per context, after the map is real); CQRS and events inside a context that needs them.
