"""Feature functions for the cohort pipeline (notebooks/cohort_pipeline.ipynb), one block per session.

    from cohort import sleep_architecture_features
    features.update(sleep_architecture_features(stages))   # stages from make_epochs: one label per 30-s epoch

Sleep architecture (Session 4) is always computed on the UNEDITED expert hypnogram: artefact rejection
(sleep_utils.bad_epochs_table) only removes epochs from the EEG features.
"""

import numpy as np
import pandas as pd
import yasa

from sleep_utils import SLEEP_STAGES

EPOCH_MIN = 30 / 60  # epoch duration in minutes: 30 seconds = 0.5 minutes
STAGES = ["WAKE", "N1", "N2", "N3", "REM"]


# ---------------------------------------------------------------- Session 4: sleep architecture
def find_bouts(h):
    """One row per bout (consecutive epochs of the same stage): stage, first epoch, number of epochs."""
    h = np.asarray(h)
    new_bout = np.r_[True, h[1:] != h[:-1]]  # True where a new bout starts
    bout_id = np.cumsum(new_bout)            # 1, 1, 1, 2, 2, 3, ...
    table = pd.DataFrame({"stage": h, "bout": bout_id, "epoch": np.arange(len(h))})
    return table.groupby("bout").agg(stage=("stage", "first"), start=("epoch", "first"),
                                     n_epochs=("epoch", "size")).reset_index(drop=True)


def transition_rate_from_stage(h, stage):
    """Transitions out of `stage` per minute spent in `stage` (NaN if the stage never occurs)."""
    h = np.asarray(h)
    n_exits = ((h[:-1] == stage) & (h[1:] != stage)).sum()
    minutes = (h == stage).sum() * EPOCH_MIN
    return n_exits / minutes if minutes > 0 else np.nan


def sleep_continuity_index(h):
    """Mean duration (min) of the bouts (consecutive epochs of the same stage) of N1, N2, N3 or REM."""
    h = np.asarray(h)
    new_bout = np.r_[True, h[1:] != h[:-1]]
    bout_stage = h[new_bout]                                     # the stage of each bout
    bout_len = np.diff(np.r_[np.flatnonzero(new_bout), len(h)])  # its length in epochs
    return bout_len[np.isin(bout_stage, SLEEP_STAGES)].mean() * EPOCH_MIN


def sleep_architecture_features(stages):
    """Sleep statistics of one night from the unedited hypnogram, as a dict.

    - YASA's sleep_statistics (TIB, TST, SE, SOL, WASO, Lat_REM, SFI, minutes and % per stage, ...)
    - Lat_REM_onset: REM latency from sleep onset (AASM); YASA's Lat_REM counts from the hypnogram start
    - shifts_per_h: stage shifts per hour of TST
    - SCI: sleep continuity index
    - rate_<stage>: transitions out of each stage per minute in that stage
    """
    stages = np.asarray(stages)
    features = dict(yasa.Hypnogram(stages, freq="30s").sleep_statistics())

    first_sleep = np.flatnonzero(np.isin(stages, SLEEP_STAGES))[0]
    rem = np.flatnonzero(stages == "REM")
    features["Lat_REM_onset"] = (rem[0] - first_sleep) * EPOCH_MIN if len(rem) else np.nan
    n_shifts = (stages[1:] != stages[:-1]).sum()
    features["shifts_per_h"] = n_shifts / (features["TST"] / 60)
    features["SCI"] = sleep_continuity_index(stages)
    for stage in STAGES:
        features[f"rate_{stage}"] = transition_rate_from_stage(stages, stage)
    return features


# ---------------------------------------------------------------- Monday: band power per stage (clean epochs)

# ---------------------------------------------------------------- Tuesday: automated staging vs. the experts

# ---------------------------------------------------------------- Wednesday: spindles and slow waves
