# Precomputed results

So that you can do the cohort exercises before (or without) running every night yourself.

- `cohort_staging.csv`: one row per night (all 153 Sleep-EDF nights): the cohort table of `notebooks/cohort_pipeline.ipynb` (Saturday's features) plus the automated-staging features of Session 6 (`staging_features`: all columns starting with `yasa_`).
- `staging_epochs.csv.gz`: one row per epoch: the night `code`, the expert stage and YASA's stage.
- `cohort_microstructure.csv`: one row per night (all 153 nights): `code, subject, night, age, sex` plus the spindle and slow-wave features of Session 7 (`microstructure_features`: columns `clean_min_*`, `sp_*`, `sw_*`).

Staging: made with YASA 0.8.1 (Fpz-Cz + horizontal EOG, no EMG, no metadata). Spindles and slow waves: YASA 0.8.1 `spindles_detect` and `sw_detect` with their default parameters, in the clean N2 and N3 epochs (`load_continuous`), Fpz-Cz and Pz-Oz. All on the nights cut by `load_subject` (lights-off to the end of the sleep period). Your own run should give the same numbers.
