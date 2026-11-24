# Session 6 · Sleep cycles: the elephant and the goldfish

**Goal:** see what an independent review by a fresh agent (the *goldfish*) finds that the agent who wrote the
code (the *elephant*) does not. The task is a real one: split each night into NREM–REM sleep cycles. The
specification and the acceptance criteria are below. You don't write the code yourself: your agent does, and you
check it.

## The exercise

| Step | What you do |
|---|---|
| 0 | Read the specification and the criteria below. Add **two synthetic test cases of your own** (criteria A). |
| 1 | **Elephant:** in your agent, on your branch: *"Implement the specification in `notebooks/session06_sleep_cycles.md`. Follow the acceptance criteria, and report how you checked each one. Don't commit."* Read the plan before you approve it. **Don't commit until step 4:** the goldfish reviews uncommitted changes. |
| 2 | **Self-review, same session:** *"Now review your own implementation against the specification and the acceptance criteria. List every problem you find, with the file and line."* Log the findings, don't fix anything yet. |
| 3 | **Goldfish, new session:** start a fresh session in the repo (Claude Code: `/clear` or a new terminal), then `/eg-precommit-review Check the changes against the specification in notebooks/session06_sleep_cycles.md`. Log the findings. |
| 4 | **Compare** steps 2 and 3. For each finding: real bug, valid caveat, or wrong? Then fix the real bugs (in either session), and commit on your branch. |
| 5 | **Shared case:** run a goldfish on the second implementation the instructor gives you, so we all compare the same code in the debrief. |

**Log (one row per finding):**

| # | Finding (short) | File:line | Self-review (2) | Goldfish (3) | Your verdict: bug / caveat / wrong |
|---|---|---|---|---|---|

Steps 2 and 3 review the *same* code. The only difference is what the reviewer knows.

---

## Specification

### What to build

A new file **`cycles.py`** in the repository folder (next to `cohort.py`), with

```python
def find_cycles(stages, min_nrem_min=15, min_rem_min=5, max_rem_gap_min=15):
    """One row per sleep cycle of a night (pandas DataFrame)."""
```

- `stages`: the stage of each 30-s epoch, as returned by `make_epochs` in `sleep_utils.py`
  (`WAKE`, `N1`, `N2`, `N3`, `REM`, `ART`, `UNS`), for the night from lights-off to the end of the sleep period
  (`load_subject`). Epoch numbers are 0-based positions in `stages`.
- It returns a DataFrame with **one row per cycle** and exactly these columns:

| Column | Meaning |
|---|---|
| `cycle` | 1, 2, 3, … |
| `start` | first epoch of the cycle |
| `rem_start` | first epoch of the REM period that ends the cycle (NaN for an incomplete cycle) |
| `end` | last epoch of the cycle (inclusive) |
| `duration_min` | number of epochs in the cycle × 0.5 (all stages, including `ART`/`UNS`) |
| `nrem_min`, `n3_min`, `rem_min`, `wake_min` | minutes of N1+N2+N3, of N3, of REM and of WAKE in the cycle |
| `complete` | `True` if the cycle ends with a REM period, `False` for the incomplete last cycle |

A night without any cycle returns an empty DataFrame **with these columns**.

### Definitions

- **NREM** = N1, N2, N3. **Sleep** = NREM + REM. `ART` and `UNS` are neither NREM, REM nor WAKE.
- **Sleep onset** = the first sleep epoch of the night.
- A **REM bout** = consecutive REM epochs.

### Rules

These follow Feinberg & Floyd (1979). Where the paper leaves room, the course decides as written here.

1. **The first cycle starts at sleep onset.** Epochs before sleep onset belong to no cycle.
2. **REM periods:** two REM bouts belong to the same REM period if fewer than `max_rem_gap_min` (15 min = 30
   epochs) of non-REM epochs separate them. *Any* epochs count in the gap: NREM, WAKE, `ART`, `UNS`. A gap of
   exactly 15 min separates two REM periods.
3. **A REM period ends a cycle** if both:
   - (a) the cycle so far (from its start to the first epoch of this REM period) contains at least
     `min_nrem_min` (15 min) of NREM, and
   - (b) the REM period contains at least `min_rem_min` (5 min) of REM. **Exception:** in the first cycle, a REM
     period of any length is enough.
4. A complete cycle runs from its start to the **last REM epoch** of the REM period that ends it. The next cycle
   starts at the epoch after that.
5. A REM period that does **not** end a cycle simply stays inside the current cycle.
6. **WAKE stays inside the cycle** in which it occurs. Cycles are never split by wake, however long.
7. **After the last complete cycle:** the remaining epochs form an **incomplete cycle** (`complete=False`) if they
   contain at least `min_nrem_min` of NREM; otherwise they belong to no cycle.
8. Use ≥ for the minimum durations and < for the REM gap, exactly as written above.

**Out of scope:** splitting very long NREM periods ("skipped" REM periods), and any special treatment of long
awakenings. Both happen in our data: report them (criteria B), don't fix them.

---

## Acceptance criteria

### A. Synthetic hypnograms with a known answer

A test script **`test_cycles.py`** (repository folder, plain `assert` statements, no new packages), run with
`uv run python test_cycles.py`. Each case is a list of (stage, number of epochs). Expected cycles as
`start–end` (epochs, inclusive), the REM start, complete or not.

| Case | Hypnogram (stage × epochs) | Expected cycles |
|---|---|---|
| A · basic | WAKE 10, N2 40, REM 20, N2 60, REM 20, N2 30 | 10–69 (REM 50) · 70–149 (REM 130) · 150–179 incomplete |
| B · REM gap < 15 min | N2 40, REM 10, N2 20, REM 10, N2 10 | 0–79 (REM 40); the last 5 min of N2 are no cycle |
| C · REM gap = 15 min | N2 40, REM 10, N2 30, REM 10 | 0–49 (REM 40) · 50–89 (REM 80) |
| D · short REM later | N2 40, REM 20, N2 40, REM 6, N2 40, REM 20 | 0–59 (REM 40) · 60–165 (REM 146), with `rem_min` 13 |
| E · short first REM | N2 40, REM 4, N2 60, REM 20 | 0–43 (REM 40) · 44–123 (REM 104) |
| F · REM too early | N1 4, N2 16, REM 20, N2 60, REM 20 | 0–119 (REM 100), with `rem_min` 20 |
| G · wake inside | N2 20, WAKE 80, N3 20, REM 20 | 0–139 (REM 120), `wake_min` 40, `n3_min` 10 |
| H · no REM | WAKE 10, N2 100 | 10–109 incomplete |
| I · too little sleep | WAKE 10, N2 20, WAKE 10 | none (empty table, all columns) |
| J · wake splits REM | N2 40, REM 10, WAKE 10, REM 10 | 0–69 (REM 40), `wake_min` 5 |
| K · short tail | N2 40, REM 20, N2 20, WAKE 40 | 0–59 (REM 40); the tail is no cycle |
| yours | two more cases of your own: what else could go wrong? | |

Check every column for at least cases A, D and G, not only the start and end.

### B. Real nights

1. **SC4002 (33 years):** on Saturday you counted about 5 cycles by eye, with REM periods ending around 23:10,
   00:20–00:50, 02:05, 03:20–03:55 and 05:15–05:35. Report the number of complete cycles and the clock time at
   which each ends (`epoch_onsets` in `sleep_utils.py`), and explain every difference from Saturday's count by a
   rule above.
2. **A figure** per night: the hypnogram with the cycle boundaries drawn in (and the incomplete cycle marked), for
   SC4002, SC4752 (96 years), and **one night for each edge case**: interrupted REM, a first REM period shorter
   than 5 min, an awakening ≥ 30 min inside a cycle, no N3. Name the night chosen for each, and why. Save the
   figures in `results/cycles/`.
3. **All 153 nights** run without errors. Save one row per cycle, with the night `code` and `age`, in
   `results/cycles_cohort.csv`.
4. **Summary** over the cohort: complete cycles per night (median and range), cycle duration (median and range).
   **List** the nights with 0 complete cycles, and every cycle shorter than 30 min or longer than 180 min. Look
   at three of the long ones in a figure: what makes them long?
5. **Plausibility, not proof:** in people under 40, N3 minutes should be highest in cycle 1 and fall across the
   cycles, and REM minutes should be lower in cycle 1 than later. Show it (a table or a figure, with n).
6. Every number comes with the number of nights and people behind it.

### C. Code

- Only new files: `cycles.py`, `test_cycles.py`, and code for the figures and the cohort run (a script or a new
  notebook). **No changes** to `sleep_utils.py`, `cohort.py`, or anything in `data/`.
- Loading with `load_subject` and `make_epochs` (only the stages are needed, so one EEG channel is enough).
- No new packages. Runs with `uv run python …`.
- The docstring of `find_cycles` states the rules (short) and cites Feinberg & Floyd (1979).

### D. The report

For each criterion above: **how** it was checked, and the **result with numbers**. "Not checked" is an
acceptable answer; "it works" is not.

---

## Background

- Feinberg I, Floyd TC (1979). Systematic trends across the night in human sleep cycles.
  *Psychophysiology* 16:283–291.
- Blume C, Cajochen C (2021). 'SleepCycles' package for R: a free software tool for the detection of sleep cycles
  from sleep staging. *MethodsX*.
