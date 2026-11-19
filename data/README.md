# Data

Unzip the course data into this folder, so that the
`*-PSG.edf` and `*-Hypnogram.edf` files are inside `data/`.

Source: Sleep-EDF Expanded, Sleep Cassette (PhysioNet, https://physionet.org/content/sleep-edfx/).
Data files are not tracked by git.

## `SC-subjects.csv` (tracked in git)

One row per night: `subject, night, age, sex_F, LightsOff`
(`sex_F`: 1 = female, 2 = male, as in the original; `LightsOff`: clock time of lights-off).

Converted from `SC-subjects.xls` of Sleep-EDF Expanded v1.0.0 (PhysioNet).
Changes: converted to CSV; column `sex (F=1)` renamed to `sex_F`. Values unchanged.

Licence: [Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/).
Please cite:
- Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, Oberyé JJL. Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. *IEEE Trans Biomed Eng* 47(9):1185–1194 (2000).
- Goldberger A, et al. PhysioBank, PhysioToolkit, and PhysioNet. *Circulation* 101(23):e215–e220 (2000).
