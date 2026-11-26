# Session 9: your cohort dashboard (Streamlit)

Today you turn the cohort results into **an app that you can open in the browser**, filter, and show to others.
You build your own dashboard, with your own choice of focus.

**Time:** about 3 h of building, then the dashboard goes into your presentation.

## 1. Get started (5 min)

Get the latest course files and install Streamlit (it is now part of the course environment), from the course
folder (`sleep-eeg-analysis`):

```bash
git pull
uv sync
```

Then start the starter app:

```bash
uv run streamlit run app/app_starter.py
```

A browser tab opens at `http://localhost:8501`. You see one graph: **% N3 against age**, one dot per night.

- **Edit and save** `app_starter.py`: the page offers *Rerun* (click *Always rerun* to see changes right away).
- **Stop** the app with `Ctrl+C` in the terminal.
- If no tab opens, open `http://localhost:8501` yourself.

## 2. The data

The starter reads `precomputed/cohort_features.csv`: **one row per night** (153 nights, 78 people), 244 columns.

| Columns | Content |
|---|---|
| `code, subject, night, age, sex` | who and which night (`sex` is `F` or `M`) |
| `TIB … SCI`, `%N1 … %REM`, `WASO`, `SE`, `SOL` | sleep statistics from the expert hypnogram (Session 4) |
| `<band>_<abs\|rel>_<stage>_<Fpz\|Pz>` | band power per stage and channel (Session 5) |
| `sp_*`, `sw_*` | spindles and slow waves (Session 8) |
| `yasa_*` | automated staging and its agreement with the expert (Session 7) |
| `pct_bad`, `n_clean_*` | data quality |

Full description: `precomputed/README.md`. To use **your own** table, change `DATA_FILE` at the top of the app to
`results/cohort_features_final.csv`.

## 3. Streamlit in 2 minutes

Streamlit **re-runs your whole script, top to bottom, every time the user touches a widget.** A widget returns its
current value:

```python
age_min = st.slider("Minimum age", 20, 100, 20)       # returns a number
data = cohort[cohort["age"] >= age_min]                # use it like any variable
```

| You want | Use |
|---|---|
| Title, text, small note | `st.title`, `st.write`, `st.markdown`, `st.caption` |
| Drop-down, radio buttons, checkbox | `st.selectbox`, `st.radio`, `st.checkbox`, `st.multiselect` |
| Slider (a range if you pass a tuple) | `st.slider("Age", 20, 100, (20, 100))` |
| Filters in a side panel | `st.sidebar.slider(...)` or `with st.sidebar:` |
| Side-by-side layout | `col1, col2 = st.columns(2)` then `with col1:` |
| Tabs | `tab_a, tab_b = st.tabs(["A", "B"])` then `with tab_a:` |
| A matplotlib figure | `st.pyplot(fig)` (the same `fig, ax = plt.subplots()` as in the notebooks) |
| A table | `st.dataframe(df)` |
| Big number | `st.metric("People", 78)` |
| Don't reload data at every click | put `@st.cache_data` above the function that reads the file |
| Stop if nothing is selected | `st.stop()` |


## 4. Suggested path

1. **Run the starter.** Change the y variable in the code (`"%N3"` → `"SE"`) and watch the graph change.
2. **Add a widget:** `st.selectbox` to choose the variable (this is the first step from a script to an app).
3. **Add filters** in the sidebar: age range, sex.
4. **Add a second graph** (e.g. a box plot per age group, or band power per stage).
5. **One person in the cohort:** select a night, highlight it among all the others.
6. **Your own question.** What do *you* want to show someone in two minutes?
7. Polish: axis labels with units, `n` on every figure, a sentence of interpretation under each graph.

*(Required panels: to be announced.)*

## 5. Good figures, and traps

- **Label axes with units**, say **what is plotted** and **how many nights/people** (`n = …`).
- **Colour-blind-safe colours** (the starter uses the Okabe-Ito palette). Don't rely on red vs green.
- **The two nights of a person are not independent.** Choose one: average per person, use night 1 only, or say
  clearly that you plot nights. Report it on the figure or under it.
- **Show the individual points** when n is small, not only means.
- **Age effects ≠ cohort effects:** this is cross-sectional data of different people, not people followed over time.
- A **correlation** is not a result until you have checked what is behind it: an outlier, a bad night, one age group.
- Check at least one number against something you know (e.g. SC4002: TST 472 min, SE 92.3 %).
