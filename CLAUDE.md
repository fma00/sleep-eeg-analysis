# Sleep EEG Analysis (Cajal course)

Course repository for "Sleep EEG Analysis: From Signal Processing to Machine Learning and Deep Learning"
(Cajal course "Neurobiology of Sleep", Bordeaux 2026). Students analyse the Sleep-EDF Sleep Cassette data:
153 nights from 78 healthy adults aged 25–101, most of them recorded on two nights.

## Who you are working with

The students are sleep researchers, not software engineers. Most of them come from MATLAB or R and are new to
Python. So:
- Explain what you do and why, in plain language. Name the sleep or signal-processing concept behind a choice.
- Write simple, readable code in the style of the existing files: numpy/pandas, short functions, a short
  docstring, comments that explain *why*. No classes, frameworks or clever one-liners unless asked.
- When a decision is scientific (a definition, a threshold, which nights to include), don't pick silently:
  ask, or state the choice clearly so the student can disagree.

## Layout

- `sleep_utils.py`: loading and preprocessing (load a night, 30-s epochs, artefact detector). **Use it**
  instead of re-implementing loading or cropping.
- `cohort.py`: feature functions for the cohort pipeline, one block per session.
- `notebooks/sessionXX_<topic>.ipynb`: the exercises. Cells with `TODO` are for the student to complete.
- `notebooks/cohort_pipeline.ipynb`: runs the features on all nights into one table (one row per night).
- `solutions/`: solution notebooks, published after each session.
- `precomputed/`: the instructor's precomputed cohort results (read-only), see its README.
- `data/`: the EDF files (not in git) and `SC-subjects.csv` (in git). **Never modify anything in `data/`.**
- `results/`, `database.csv`: the student's own outputs and choice of nights (not in git).

## Running code

- Always through the course environment: `uv run python <script>`, or the `.venv` kernel in notebooks.
- Don't add or upgrade packages unless the student asks; then use `uv add <package>` (never `pip install`).
- Running all 153 nights takes minutes. Test on a few nights first (e.g. SC4001, SC4002), then run the cohort.

## Data facts

- File names: `SC4<subject:02d><night>*-PSG.edf` and `*-Hypnogram.edf`, e.g. SC4002 = subject 0, night 2.
- EEG Fpz-Cz and Pz-Oz at 100 Hz, plus EOG (`horizontal`) and EMG (`submental`). MNE returns volts:
  use `get_data(units="uV")` for µV.
- `SC-subjects.csv`: **one row per night**, keyed by `(subject, night)`: `subject, night, age, sex_F, LightsOff`.
  `sex_F`: 1 = female, 2 = male. `LightsOff` is a clock time; after midnight it belongs to the next day.
- Recordings start in the afternoon and run ~20 h, into the next day. The hypnogram runs past the end of the EEG.

## Course conventions

These are decisions made in the course. Follow them, and say so when you rely on one. If a student wants to
deviate, that's fine, but it must be explicit and documented.

**The night**
- From lights-off (`SC-subjects.csv`) to the last sleep epoch before the first wake period of ≥ 180 min
  (`load_subject`). This leaves out naps the next day.

**Stages**
- Labels: `WAKE, N1, N2, N3, REM`, plus `ART` (R&K "Movement time") and `UNS` (unscored).
  R&K stages 3 and 4 are both N3. Sleep = N1, N2, N3, REM. `ART` and `UNS` are neither sleep nor wake.

**Sleep statistics**
- Always on the **unedited expert hypnogram**. Artefact rejection never removes epochs from sleep statistics.
- AASM definitions: SOL from lights-off to the first sleep epoch; WASO = wake after the first sleep epoch;
  REM latency from **sleep onset** (YASA's `Lat_REM` counts from the start of the hypnogram instead).
- `cohort.sleep_architecture_features` computes them for one night.

**Artefacts**
- The course detector `sleep_utils.artifact_rejection` (after Mariani et al., 2018): an epoch is bad if its
  0.5–4.5 Hz power is > 2.5× or its 20–40 Hz power is > 2× the mean of the ± 7 epochs around it (Fpz-Cz and
  Pz-Oz). Bad = detector OR `ART`. Bad epochs are only removed from **EEG features** (spectra, band power,
  spindles, slow waves).
- `sleep_utils.load_epochs` does it all: load, filter EEG/EOG 0.1–40 Hz, 30-s epochs, table of bad epochs.

**Spectra**
- Welch with 2-s windows (scipy defaults otherwise: Hann, 50 % overlap), in µV²/Hz.
- Bands: delta 0.5–4, theta 4–8, alpha 8–12, sigma 12–16, beta 16–30, gamma 30–40 Hz.
  Band power = area under the PSD (Simpson); relative power = band / total power 0.5–40 Hz.

**Spindles and slow waves**
- YASA `spindles_detect` / `sw_detect` on the continuous signal from `sleep_utils.load_continuous` (its per-sample
  hypnogram has −1 in the bad epochs, so only clean epochs are searched), in N2 and N3.
- The cohort features use YASA's **default parameters** (`microstructure_features`, Session 7). Density = events
  per minute of clean N2 or N3. Any other threshold is a scientific choice: state it, and keep the default
  version for comparison. YASA's spindle thresholds are mostly relative to the night's own signal, its
  slow-wave thresholds are absolute (µV).

**Cohort analyses**
- Most people have two nights. A night is not an independent person: average per person, use one
  predefined night, or model the person explicitly. Say which.
- Which nights are included is recorded in `database.csv` (`include`, `exclude_reason`). Every exclusion
  needs a reason.

## Check your results

Before reporting a result, check it against something known:
- SC4002 (33 years): TST 472 min, SE 92.3 %, 53 bad epochs (5.2 %).
- Plausible ranges: N3 delta power in the hundreds of µV²; %N3 drops with age; SE and WASO get worse with age.
- Show the number of nights and people behind every number.
Say what you checked and what you did not. "It runs" is not "it is correct".

## Exercises and solutions

- When a student asks for help with a `TODO`, help them learn: explain the idea and give a hint first.
  Give the full answer when they ask for it.
- Don't open `solutions/` unless the student asks you to.

## Git

- `origin` is the course repository: students only pull from it. Their own work is on their branch
  (e.g. `my-work`) and goes to their private GitHub repository (remote `mine`).
- Never commit or push unless the student asks. Never push to `origin`.
- Put new analyses in **new files** (e.g. a new module next to `cohort.py`) rather than rewriting
  `sleep_utils.py` or `cohort.py`: the instructor updates those during the week, and students pull the changes.

## Privacy

Sleep-EDF is public. If a student works with their own recordings, those may be patient or animal data that
must not leave their computer: ask before sending any of it to an online service.

## Elephant/Goldfish workflows

`.claude/commands/` has six workflows. They keep this session's context (the elephant) and send the
review work to fresh agents without that context (the goldfish), which catch assumptions this session has
stopped questioning. Use them only when the student asks:

| Workflow | Use it for |
|---|---|
| `/eg-question` | A short answer grounded in the code or sources. Read-only. |
| `/eg-brainstorm` | Different approaches to a rough idea. |
| `/eg-prd` | Requirements, open questions and optional session-sized tasks. |
| `/eg-new-feature` | Design, fresh reviews, implementation and checks. |
| `/eg-fix-bug` | Independent diagnosis, a failing regression test and a fix. |
| `/eg-precommit-review` | An independent review of staged, unstaged and untracked changes. |

Fresh reviewers receive only the evidence for their task. A missing dispatch or missing evidence means the
review is incomplete, not clean. These workflows cost extra time and tokens: for small questions and edits,
just answer.
