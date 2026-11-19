# Data

We use the **Sleep Cassette** part of **Sleep-EDF Expanded** (PhysioNet, https://physionet.org/content/sleep-edfx/1.0.0/):
153 nights from 78 healthy adults aged 25–101, recorded at home. Each night has a `*-PSG.edf` file (EEG Fpz-Cz and Pz-Oz,
EOG, EMG, …, ~50 MB) and a `*-Hypnogram.edf` file (expert sleep scoring).
Data files are not tracked by git.

## During the course
You'll get the data **on a USB stick during the course**. Copy it into this `data/` folder (unzip it first if it's a zip),
so that the `*-PSG.edf` and `*-Hypnogram.edf` files are inside `data/` (subfolders are fine).
`check_setup.py` works without data too (it then uses a synthetic signal), so you can finish the setup while the copy runs.

## After the course: downloading the data yourself
The data are freely available. Downloading straight from PhysioNet is slow (about 3 minutes per night), so start with a few nights.

**Option 1: with MNE (works on all systems).** Run this in the repository folder:
```bash
uv run python -c "import mne; mne.datasets.sleep_physionet.age.fetch_data(subjects=[0, 1, 2], recording=[1, 2], path='data', on_missing='warn')"
```
- `subjects`: subject numbers 0–82 (some numbers don't exist), see `SC-subjects.csv` for age and sex
- `recording`: night 1 and/or 2 (a few subjects have only one night; `on_missing='warn'` skips those)
- the files end up in `data/physionet-sleep-data/`

**Option 2: the full Sleep Cassette set (~7.5 GB)**
- Linux (or macOS after `brew install wget`): `wget -r -N -c -np -nH --cut-dirs=3 -P data https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/`
- or download the complete Sleep-EDF Expanded ZIP (~8 GB) from the "Files" section of https://physionet.org/content/sleep-edfx/1.0.0/ and copy the `sleep-cassette` folder into `data/`.

## `SC-subjects.csv` (tracked in git)

One row per night: `subject, night, age, sex_F, LightsOff`
(`sex_F`: 1 = female, 2 = male, as in the original; `LightsOff`: clock time of lights-off).

Converted from `SC-subjects.xls` of Sleep-EDF Expanded v1.0.0 (PhysioNet).
Changes: converted to CSV; column `sex (F=1)` renamed to `sex_F`. Values unchanged.

Licence: [Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/).
Please cite:
- Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, Oberyé JJL. Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. *IEEE Trans Biomed Eng* 47(9):1185–1194 (2000).
- Goldberger A, et al. PhysioBank, PhysioToolkit, and PhysioNet. *Circulation* 101(23):e215–e220 (2000).
