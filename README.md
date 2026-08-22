# DelayGuard 360

**From delay detection to delay prevention.**

Predicts SLA breaches before they happen, explains why a request is at risk,
recommends preventive action, and prioritizes what needs attention first —
built as a multi-page Streamlit app with role-based dashboards.

## What's included

| Page | What it does |
|---|---|
| `app.py` | Landing page + system-wide KPI overview |
| `pages/1_Login.py` | Role selection (Admin / Manager / Employee / Citizen) + demo access |
| `pages/2_Admin_Dashboard.py` | Full system visibility: KPIs, SLA trend, department performance, risk distribution |
| `pages/3_Manager_Dashboard.py` | Team workload, critical requests, escalate/reassign/approve actions |
| `pages/4_Employee_Dashboard.py` | Personal queue, due-today requests, stage updates |
| `pages/5_Citizen_Portal.py` | Submit a request, track status |
| `pages/6_Risk_Analysis.py` | Explainable AI: risk gauge, score breakdown, reasons, recommendations |
| `pages/7_Bottleneck_Analytics.py` | Bottleneck heat map by department × stage |
| `pages/8_Recovery_Simulator.py` | Predicts the effect of corrective action (extra staff, priority boost) |
| `pages/9_Notification_Center.py` | High-risk, critical, and escalation alerts |

The AI logic (`utils/`) implements the spec's rule-based engines directly —
no external model calls, so it runs anywhere with no API keys:

- `risk_engine.py` — Risk Score = 40% SLA usage + 30% stage delay history + 20% department delay history + 10% priority impact
- `explain.py` — turns the score into plain-language reasons
- `recommend.py` — rule-based next-action suggestions
- `data_gen.py` — generates a consistent mock dataset of 100 requests (cached, seeded)

## Run it locally

```bash
git clone https://github.com/YOUR_USERNAME/delayguard360.git
cd delayguard360
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## Push to GitHub

```bash
cd delayguard360
git init
git add .
git commit -m "Initial commit: DelayGuard 360"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/delayguard360.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Pick your `delayguard360` repo, branch `main`, and main file path `app.py`.
4. Click **Deploy**.

Streamlit Cloud installs `requirements.txt` automatically and picks up
`.streamlit/config.toml` for the dark theme. No secrets or API keys are
needed since everything runs on the built-in mock dataset and rule-based
engines.

## Notes

- The dataset is generated with a fixed random seed, so numbers stay
  consistent across pages and across app restarts.
- Login is a UI simulation — no real authentication is performed.
- To reset/regenerate mock data, clear Streamlit's cache from the app menu
  (top-right ⋮ → **Clear cache**) and rerun.
