# Enhance map: <target skill>

Private. Keep this file in the ignored scratch folder. Do not commit it and do not copy it into the catalog.

```
Target:            <path to the skill folder>
Policy:            <upstream names in shipped files: none | allowed>. <language>. <vocabulary bar>
Do not remove:     <template, step order, command, file>
Scratch folder:    <path> (ignored by git: yes | no)
Baseline:          lint <n errors, n warnings>. tests <n pass, n fail>
```

## Source: <name> (<url>, read <date>, read to the end: yes | partly)

| Method | Choice | Where it goes | Note |
|---|---|---|---|
| <what it does, in one line> | keep | `<target path or sibling skill>` | <how we write it differently> |
| <what it does> | replace | `<new file or script>` | <what we build instead, and why the original form does not fit> |
| <what it does> | drop | none | <reason: off the job, other owner, trend, unsafe, license> |

## Ownership

| Method | Owner skill | Pointer updated in |
|---|---|---|
| <method> | `<skill>` | `<sibling files>` |

## Result

- New files: <list>
- Changed files: <list>
- Description changed: yes | no
- Checks: lint <result>. tests <result>. Built output opened and used: yes | no
- Not verified: <list>
