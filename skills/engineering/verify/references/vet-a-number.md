# Vet a number

Use this before you report a number you measured: a speedup, a slowdown, a latency, a throughput, a benchmark, or a pick between two libraries or settings. Check the number with evidence from a run. A guess about the code is not evidence.

## Contents
- Before the run
- Five checks
- A quick ballpark
- The report

## Before the run

1. **Write the sentence you plan to publish.** For example: "The export is 30% faster at p50 on the 60k-row dataset." Every check below tests that sentence.
2. **Read the measuring script.** What does it time? What does it count? What does it skip?
3. **Look at the machine.** Check the load (`uptime`) and the core count (`nproc`, or `sysctl -n hw.ncpu` on macOS). If it is busy, find out why. If you cannot stop the load, alternate the runs so both sides get the same noise, and say so.

## Five checks

### 1. Fair
Both sides must run the same way. Same build mode, flags, environment, data, versions and cache state. Same batch and pool settings. Production settings, not defaults.

If one side ran on defaults, you compared settings, not code. A limiter that is only a setting (a commit per row, a debug build, a missing index) means that side is untuned. Tune it and measure again. If you cannot tune it, do not name a winner.

### 2. Real
The work you think you timed must have happened inside the timer.
- The request reached the server. The rows were written. The result was used.
- Watch for lazy code: a generator nobody reads, a promise nobody awaits, a result the compiler drops.
- Count errors, rejections and timeouts. Failures are often very fast, or very slow, and they skew the number.
- Check that the output is correct, not only present.

### 3. Steady
Run each side at least 5 times. Alternate them: A, B, A, B. Report the median and the range. If the gap between sides is smaller than the spread of runs, there is no measurable difference. For a close call, use a rank-sum test or the harness's own statistics.

### 4. Bounded
Find what limits the number. Profile in a run you will not report, because profilers slow things down. Look at CPU per process, a runtime profiler (`node --cpu-prof`, `py-spy`, `perf`), I/O wait and syscalls. Watch the load generator too. If it maxes out first, you measured the load generator.

Then do the arithmetic against hard limits:
- Bytes per second against disk and network speed.
- Operations per second times the cost of one operation, against your cores.
- The best possible gain. If the piece you changed takes 10% of the run, the run can get at most about 11% faster.

A result past a hard limit measured something else, such as a cache, a no-op or a bug.

### 5. Relevant
Next to any micro result, measure the whole path a user waits on, with realistic data size and load. Give the micro result as a share of that whole. A helper that is 1% of a request cannot make the request more than 1% faster.

## A quick ballpark

If the user only wants a rough number, one run is fine. Still do check 2 (errors and real work), and say it was one run. Skip the rest unless that run looks odd. A choice between options is never a ballpark.

## The report

- Start with a verdict word: **faster**, **slower**, **no measurable difference** or **inconclusive**.
- Then the number with its unit, the run count, the range and the limiter. Example: "p50 41 ms to 33 ms. Median of 7 runs per side. Range 32 to 35 ms. Bound by JSON parsing on one core."
- Say **inconclusive** when you claim a gap but cannot name the limiter, when a side was untuned, or when you could not check for errors and real work. Name the gap.
- A PR body gets one main number. Put runs, range and limiter evidence in a linked note.
