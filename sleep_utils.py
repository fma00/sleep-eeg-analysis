"""Helper functions for the course notebooks (from Session 3 on).

These do what you did step by step in Session 2, so everyone starts from the same data:

    from sleep_utils import load_subject, make_epochs
    raw = load_subject(0, 2)            # SC4002, cropped from lights-off to the end of the sleep period
    epochs, stages = make_epochs(raw)   # 30-s epochs + the expert stage of each one
"""

import os
from pathlib import Path

import mne
import numpy as np
import pandas as pd

# The EDF files: data/ in the repo, or another folder (e.g. an external drive) set in the environment variable
# SLEEP_DATA_DIR. Subfolders are fine. The subject table always comes from the repo.
DATA_DIR = Path(os.environ.get("SLEEP_DATA_DIR", Path(__file__).parent / "data"))
SUBJECTS_CSV = Path(__file__).parent / "data" / "SC-subjects.csv"

# Sleep-EDF (R&K) labels -> the short AASM/YASA labels we use in the course
STAGE_NAMES = {
    "Sleep stage W": "WAKE",
    "Sleep stage 1": "N1",
    "Sleep stage 2": "N2",
    "Sleep stage 3": "N3",  # R&K stages 3 and 4 -> AASM N3
    "Sleep stage 4": "N3",
    "Sleep stage R": "REM",
    "Sleep stage ?": "UNS",  # unscored
    "Movement time": "ART",  # artefact
}
SLEEP_STAGES = ["N1", "N2", "N3", "REM"]
EVENT_ID = {"WAKE": 1, "N1": 2, "N2": 3, "N3": 4, "REM": 5, "ART": 6, "UNS": 7}  # stage -> event id


def night_code(subject, night):
    """Sleep-EDF file prefix of a night, e.g. (0, 2) -> "SC4002"."""
    return f"SC4{subject:02d}{night}"


def clock_to_seconds(clock, raw):
    """Seconds from the first sample of `raw` to a clock time like "21:57:00"."""
    first = pd.Timestamp(raw.info["meas_date"]) + pd.Timedelta(seconds=raw.first_time)
    t = pd.Timestamp(f"{first.date()} {clock}", tz=first.tz)
    if t < first:  # e.g. 00:38 is on the next day
        t += pd.Timedelta(days=1)
    return (t - first).total_seconds()


def load_subject(subject, night, data_dir=DATA_DIR, crop=True, max_wake_min=180):
    """Load one Sleep-EDF night as an MNE Raw with the expert hypnogram as annotations.

    - channel types fixed ("Event marker" -> misc), stages renamed to WAKE/N1/N2/N3/REM/ART/UNS
    - crop=True: cropped from lights-off (SC-subjects.csv) to the end of the sleep period
    - not filtered: that's your choice

    There is no lights-on time, so the end of the night is a choice. Ours: the sleep period ends with the last
    sleep epoch before the first wake bout (no N1-REM) of at least `max_wake_min` minutes. This leaves out
    naps the next day (e.g. SC4731 would otherwise run until 14:04). In Sleep-EDF, all wake bouts of 3 h or more
    start after 06:00, and nocturnal awakenings last up to ~2.5 h (SC4601), hence 180 min.
    """
    data_dir = Path(data_dir)
    code = night_code(subject, night)
    psg_file = next(data_dir.rglob(f"{code}*-PSG.edf"), None)
    hyp_file = next(data_dir.rglob(f"{code}*-Hypnogram.edf"), None)
    if psg_file is None or hyp_file is None:
        raise FileNotFoundError(f"No EDF files for {code} in {data_dir.resolve()}")

    raw = mne.io.read_raw_edf(psg_file, preload=True, infer_types=True, verbose="ERROR")
    raw.set_channel_types({"Event marker": "misc"}, on_unit_change="ignore")
    raw.set_annotations(mne.read_annotations(hyp_file), emit_warning=False)
    present = set(raw.annotations.description)
    raw.annotations.rename({old: new for old, new in STAGE_NAMES.items() if old in present})

    if crop:
        subjects = pd.read_csv(SUBJECTS_CSV)
        row = subjects[(subjects["subject"] == subject) & (subjects["night"] == night)]
        t_lights_off = clock_to_seconds(row["LightsOff"].iloc[0], raw)
        sleep = raw.annotations[np.isin(raw.annotations.description, SLEEP_STAGES)]
        onsets = sleep.onset - raw.first_time  # s from the first sample
        ends = onsets + sleep.duration
        keep = ends > t_lights_off  # sleep after lights-off
        onsets, ends = onsets[keep], ends[keep]
        long_wake = np.flatnonzero(onsets[1:] - ends[:-1] >= max_wake_min * 60)  # gaps between sleep annotations
        end = ends[long_wake[0]] if len(long_wake) else ends[-1]
        raw.crop(tmin=t_lights_off, tmax=min(end, raw.times[-1]))  # some scorings end with the recording
    return raw


def make_epochs(raw, picks=("Fpz-Cz", "Pz-Oz", "horizontal", "submental")):
    """Cut `raw` into 30-s epochs that follow the hypnogram.

    Returns the mne.Epochs and a numpy array with the stage of each epoch ("WAKE", "N2", ...).
    """
    events, event_id = mne.events_from_annotations(raw, event_id=EVENT_ID, chunk_duration=30.0, verbose="ERROR")
    event_id = {k: v for k, v in event_id.items() if v in events[:, 2]}  # only the stages that have whole epochs
    sfreq = raw.info["sfreq"]
    epochs = mne.Epochs(raw, events, event_id, tmin=0, tmax=30 - 1 / sfreq, baseline=None,
                        picks=list(picks), preload=True, verbose="ERROR")
    id_to_stage = {v: k for k, v in event_id.items()}
    stages = np.array([id_to_stage[i] for i in epochs.events[:, 2]])
    return epochs, stages


def epoch_onsets(epochs):
    """Clock time (pd.Timestamp) of the start of each epoch, as in the Session 2 table."""
    sfreq = epochs.info["sfreq"]
    return pd.Timestamp(epochs.info["meas_date"]) + pd.to_timedelta(epochs.events[:, 0] / sfreq, unit="s")
