# Split independent tasks

Use Split when tasks are separable by file, subsystem, question, or output artifact and can finish without reading each other's work.

1. Make a dependency and overlap table. Put related failures in one seat. If two seats would change the same source or need the same mutable state, redraw the boundary or run them in sequence.
2. Assign one bounded task per seat. Name its input, the paths it owns, the expected artifact, and the check it should run. Keep a shared acceptance condition for the combined result.
3. Dispatch the seats at once. A read-only investigator reports evidence and a recommendation. A writing worker uses its own worktree or output folder and reports its changed files and observed checks; it does not merge, commit, publish, or delete on the coordinator's behalf.
4. After all seats return, read their changes and reports. Check each claimed fix, overlapping edits, and any cross-task behavior. Integrate only non-conflicting changes into one final artifact. On conflict or moved base, stop automatic integration and resolve the cause deliberately.
5. Run checks that cover the combined result, then hand it to the shared `evidence` Judge gate in [SKILL.md](../SKILL.md).

Example: three unrelated test failures in separate subsystems can get three focused workers. Three failures caused by one changed API contract belong to one investigation first.
