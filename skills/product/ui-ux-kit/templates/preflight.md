# Interface preflight: <screen>

Fill every line with pass, fail, or not verified plus the evidence. Evidence is a render, a device run, a test or a source line.

## Process

- [ ] Ran on the smallest supported phone and in landscape
- [ ] Ran with the largest system text size
- [ ] Ran with reduced motion on
- [ ] Ran in light and in dark, each measured on its own
- [ ] Ran with the screen reader on the main task
- [ ] Checked on a real device for gestures, haptics, refresh rate and performance (or said it was not)

## Platform

- [ ] Targets meet the minimum for the platform
- [ ] Navigation follows the platform model and system back works
- [ ] Safe areas, insets and the keyboard are handled
- [ ] Wide windows restructure and do not stretch
- [ ] Car: each task fits in two or three glances and the template is used
- [ ] TV: every item is reachable by remote and focus is obvious

## Quality

- [ ] One question answered by the biggest block, and the finding stated
- [ ] Every state exists: default, hover or focus, pressed, disabled, loading, empty, error, offline
- [ ] No raw hex, no raw sizes, only tokens
- [ ] Motion has a purpose, a duration token and a reduced-motion path
- [ ] Gesture actions have an alternative
- [ ] Forms have labels, hints and errors next to fields
- [ ] Content is real and believable

## Report

`ux-acceptance.csv` rows written: <count>. Not verified: <list>.
