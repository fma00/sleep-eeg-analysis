# Precomputed results

So that you can do the cohort exercises before (or without) running every night yourself.

- `cohort_staging.csv`: one row per night (all 153 Sleep-EDF nights): the cohort table of `notebooks/cohort_pipeline.ipynb` (Saturday's features) plus the automated-staging features of Session 6 (`staging_features`: all columns starting with `yasa_`).
- `staging_epochs.csv.gz`: one row per epoch: the night `code`, the expert stage and YASA's stage.
- `cohort_microstructure.csv`: one row per night (all 153 nights): `code, subject, night, age, sex` plus spindle and slow-wave features (columns `clean_min_*`, `sp_*`, `sw_*`): YASA defaults with a 12–16 Hz spindle band, clean N2 and N3 epochs, Fpz-Cz and Pz-Oz.

Staging: made with YASA 0.8.1 (Fpz-Cz + horizontal EOG, no EMG, no metadata). Spindles and slow waves: YASA 0.8.1 `spindles_detect` (spindle band 12–16 Hz, otherwise defaults) and `sw_detect` (defaults), in the clean N2 and N3 epochs (`load_continuous`), Fpz-Cz and Pz-Oz. All on the nights cut by `load_subject` (lights-off to the end of the sleep period). Your own run should give the same numbers.

- `cohort_features.csv`: **the full cohort table for the machine-learning session** (all 153 nights, one row per night, 244 columns): output of `notebooks/cohort_pipeline_final.ipynb`. Sleep statistics (Session 4), data quality, band power per stage (`<band>_<abs|rel>_<stage>_<Fpz|Pz>`, median of the clean epochs), spindles and slow waves (as `cohort_microstructure.csv`) and automated staging (`yasa_*`, as `cohort_staging.csv`, with entropy, KL divergence and intrusions). `ART` and `UNS` (counts of epochs) are 0 when the night has none; other empty cells are real missing values (e.g. no N3 or no slow waves found). Most people have two nights: for ML, keep both nights of a person in the same fold (group by `subject`).
