# Upstream: sequenced infographic choreography

Adapted ideas from [iart-ai/data-animation-skills](https://github.com/iart-ai/data-animation-skills) skill `animated-infographic` (MIT-style open reference; verify license in that repo before redistributing derived code).

| Upstream | Levistack |
|---|---|
| Remotion frame clock, MP4/GIF export | Single self-contained **SVG** with CSS keyframes only |
| `useCurrentFrame()` stagger and spring pop | Fixed delays in `build_animated_svg.py` and optional `timing` in JSON |
| Eased count-up counters | Final `value_display` strings in markup for sourced work; opacity reveal only |
| Synthetic demo count-up | Allowed only when `synthetic: true`; still no false intermediate stats in evidence mode |

Primary ports: [references/sequenced-infographic-choreography.md](references/sequenced-infographic-choreography.md), [references/animated-svg-sequenced.md](references/animated-svg-sequenced.md), [scripts/build_animated_svg.py](scripts/build_animated_svg.py).

Do not add Remotion, video encode, or MP4 deliverables to this skill.
