# SupeRR Selector Pressure Reliability Dashboard

Interactive Streamlit dashboard for the supplied player-level pressure analysis.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

## Publish a public dashboard link

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and the `data/` folder.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select the repository, branch, and `app.py` as the main file.
4. Deploy. Streamlit Community Cloud will provide a public URL that can be pasted into the competition's dashboard-link field.

## Contents
- `app.py`: interactive dashboard with batter/bowler views, sortable player data, charts, and profile explorer.
- `data/batters_ranked.csv`: player-level batting analysis output.
- `data/bowlers_ranked.csv`: player-level bowling analysis output.

## Important interpretation note
The dashboard displays the supplied ranked analysis outputs. Scores are model-based and depend on the pressure definition, weights, eligibility thresholds, and sample sizes. They are not official ratings or guarantees of future performance. Review the official challenge brief and final PDF methodology before submission.
