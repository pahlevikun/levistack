# Poetic prose

Read this only when the user asks for `prose_style: puitis`, “bahasa yang indah”, “lebih liris”, or similar. Default is **poetic prose**, not stanza verse. Write pantun, rhyme, or bound verse only when asked.

## Techniques

Poetic mode is a **style axis** (`prose_style: puitis`), not a use-case pack. Still load [natural-writing.md](../techniques/natural-writing.md) for calque cleanup.

Do not load marketing or locale marketing sections unless the user also asked for that use case.

Routing: [core.md](../core.md) § Technique routing; index [techniques/README.md](../techniques/README.md).

## Priority

1. Facts, actions, certainty, and permission
2. Clear relations between ideas
3. Imagery that helps understanding
4. Rhythm and other ornament

If ornament hurts a layer above it, delete the ornament.

## Calibration

- `tipis` — one image or rhythm turn at the open or close; the body stays plain
- `sedang` — a lyrical rhythm may shape a few paragraphs; technical steps stay literal
- `kental` — lyrical prose may dominate, but facts and actions stay easy to scan

Regional `intensity` does not set poetic density. Use `poetic_intensity`.

## For a coding agent

Start technical reports with a literal result, diagnosis, or warning. Imagery may follow after the reader knows the state.

Do not rewrite code, identifiers, commands, paths, logs, errors, or exact-match text to make them poetic. Task-target artifacts may still change if the user asked for that change.

On destructive actions, security, and permission, write the target and the effect in plain words **before** any style. A reader must not have to decode a metaphor to see the risk.

Example, `sedang`:

> `rm -rf ./build-cache` will delete everything inside `./build-cache`. I need your OK before I run it.

The command and path stay literal in the first paragraph. Imagery, if any, comes after.

## Avoid

- mixed metaphors, stacked adjectives, archaic words as decoration
- personifying every technical object
- a grand opening for a simple status
- rhyme that changes the meaning
- fake quotes or impersonating a known author
