"""Session 9: starter Streamlit app.

It loads the cohort table (one row per night) and shows ONE graph: % N3 against age.
Your job is to grow it into your own dashboard.

Run it from the course folder (sleep-eeg-analysis):
    uv run streamlit run app/app_starter.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# 1. Data
# ---------------------------------------------------------------------------
# The instructor's precomputed table. To use your own table instead, point this to
# "results/cohort_features_final.csv" (same columns, if your cohort pipeline ran on all nights).
DATA_FILE = Path(__file__).parent.parent / "precomputed" / "cohort_features.csv"

# Colour-blind-friendly colours (Okabe-Ito, lightened for the dark background) for the two sexes
SEX_COLORS = {"F": "#E69F00", "M": "#56B4E9"}

# Dark figures that match the dark page (see .streamlit/config.toml): white axes and text, bigger fonts
BACKGROUND = "#0E1117"
plt.rcParams.update({
    "figure.facecolor": BACKGROUND, "axes.facecolor": BACKGROUND, "savefig.facecolor": BACKGROUND,
    "text.color": "white", "axes.labelcolor": "white", "axes.edgecolor": "white",
    "xtick.color": "white", "ytick.color": "white",
    "legend.facecolor": BACKGROUND, "legend.edgecolor": "white", "legend.labelcolor": "white",
    "font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 13, "ytick.labelsize": 13, "legend.fontsize": 12,
    "axes.linewidth": 1.8, "axes.spines.top": False, "axes.spines.right": False,
})


@st.cache_data  # Streamlit re-runs this whole script at every click: the cache loads the file only once
def load_cohort():
    """One row per night: sleep statistics, band power, spindles, slow waves, YASA staging."""
    return pd.read_csv(DATA_FILE)


cohort = load_cohort()

# ---------------------------------------------------------------------------
# 2. Page
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Sleep-EDF cohort", layout="wide")
st.title("Sleep across the lifespan")
st.write(
    f"Sleep-EDF Sleep Cassette: **{len(cohort)} nights** from "
    f"**{cohort['subject'].nunique()} people**, aged {cohort['age'].min()}–{cohort['age'].max()} years."
)

# ---------------------------------------------------------------------------
# 3. One graph: % N3 against age, one dot per night
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4))
for sex, color in SEX_COLORS.items():
    rows = cohort[cohort["sex"] == sex]
    ax.scatter(rows["age"], rows["%N3"], color=color, alpha=0.9, s=50, label=f"{sex} (n = {len(rows)} nights)")
ax.set_xlabel("Age (years)")
ax.set_ylabel("N3 (% of total sleep time)")
ax.legend()
st.pyplot(fig)

st.caption("Most people have two nights, so the dots are not independent (see CLAUDE.md, 'Cohort analyses').")