# Game and real-time architecture

Patterns for interactive, frame-driven systems where state changes constantly and performance matters. They also fit simulations and UI-heavy clients.

## Pick when
- State machines drive behavior (characters, AI, game flow, UI modes).
- Many short-lived objects are created and destroyed (bullets, particles, enemies).
- Systems must react to events without knowing each other (UI, achievements, audio).
- Actions need undo, replay or networking.

## Avoid when
- Ordinary request and response services. Use a style from the main list.

## Patterns

| Pattern | Use for | Idea |
|---|---|---|
| **State machine** | Character states, AI, game flow, UI modes | Explicit states and transitions; one active state; entering and leaving run hooks. Prevents flag soup |
| **Object pool** | Bullets, particles, enemies, audio sources | Preallocate and reuse; reset on acquire; avoids allocation spikes and garbage-collection stalls |
| **Observer (events)** | UI updates, achievements, damage notifications | Publishers emit events; subscribers register; loose coupling. Unsubscribe on destroy |
| **Command** | Undo and redo, input replay, networking | Wrap an action as an object with `execute` and optionally `undo`; log them to replay or send them |

Entity-component-system is a common alternative to deep inheritance: entities are ids, components are data, systems are behavior over component sets. Prefer it when many entities share changing combinations of behavior.

## Layers

```
Core / engine      rendering, input, audio, physics, time, resource loading
Systems            gameplay systems: movement, combat, inventory, AI
Gameplay           game-specific rules and content wiring
Content / data     levels, balance values, definitions loaded from data files
```

Dependencies point from gameplay toward core services, and the core never knows the game. Keep the simulation separate from presentation so it can run headless in tests.

## Rules
1. **Data-driven design.** Put balance numbers, definitions and level data in data files so designers can change them without recompiling.
2. **Loose coupling.** Systems talk through events or interfaces, so each can change alone.
3. **Interface abstractions** over engine services, so logic is testable without the engine.
4. **Single responsibility** per class or system.
5. **Fixed update step** for simulation; interpolate for rendering.
6. **Measure before optimizing,** and pool only what profiling shows is hot.

## Build steps
1. List the game loop phases: input, update (fixed step), late update, render.
2. Choose the entity model (object hierarchy or ECS).
3. Model behaviors as state machines.
4. Add an event bus for cross-system notifications.
5. Add pools for frequently created objects.
6. Wrap player and AI actions as commands if undo, replay or networking is needed.
7. Load content from data files.
8. Test the simulation without rendering.

## Pitfalls
Boolean flags instead of states, allocation in the hot loop, event subscriptions never removed, systems that call each other directly, balance values hardcoded in code, simulation tied to the render frame rate.

## Combines with
Event-driven (the event bus), plugin architecture (mods), CQRS-like command logs for replay.
