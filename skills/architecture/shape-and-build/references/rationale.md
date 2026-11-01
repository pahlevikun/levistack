# Shape rationale

Keep it to one screen. Put it in the reply, or beside the code when the repo keeps design notes.

```markdown
## Shape: <change in a few words>

### Caller sketch
<the call site as real code>

### Candidates
| Candidate | Public surface | Hides | Red flags |
|---|---|---|---|
| A <name> | <types and signatures> | <what callers no longer need to know> | <none, or the flag> |
| B <name> | ... | ... | ... |

### Pick
<A or B>, because <the reason tied to the caller sketch and the red flags>.

### Deviations during build
| Where | Sketch said | Code needed | Cause: sketch wrong, missed requirement, or overreach |
|---|---|---|---|

### Scrapped
<None, or the shape, the pattern that condemned it, and what the new sketch removed>
```
