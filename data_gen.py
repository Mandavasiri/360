"""Generates the mock dataset of service requests (Deliverable 11)."""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st

from .constants import (
    STAGES,
    DEPARTMENTS,
    SERVICE_TYPES,
    OFFICERS,
    PRIORITIES,
    PRIORITY_WEIGHTS,
    SLA_HOURS,
)
from .risk_engine import compute_risk_score, risk_level, sla_usage_pct
from .recommend import delay_impact_score


@st.cache_data
def get_data(n: int = 100, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    now = datetime(2026, 8, 23, 9, 0, 0)

    rows = []
    for i in range(1, n + 1):
        department = rng.choice(DEPARTMENTS)
        service_type = rng.choice(SERVICE_TYPES[department])
        priority = rng.choice(PRIORITIES, p=PRIORITY_WEIGHTS)
        sla_hours = SLA_HOURS[priority]

        age_hours = float(rng.uniform(0, sla_hours * 1.6))
        request_date = now - timedelta(hours=age_hours)

        elapsed_fraction = min(age_hours / sla_hours, 1.4)
        stage_idx = int(np.clip(round(elapsed_fraction * 5 + rng.normal(0, 0.6)), 0, 5))
        current_stage = STAGES[stage_idx]

        officer = rng.choice(OFFICERS)
        sla_deadline = request_date + timedelta(hours=sla_hours)

        if current_stage == "Completion":
            status = "Completed"
        elif age_hours > sla_hours:
            status = "Overdue"
        else:
            status = "In Progress"

        sla_pct = sla_usage_pct(age_hours, sla_hours)
        score = compute_risk_score(age_hours, sla_hours, current_stage, department, priority)
        level = risk_level(score)

        rows.append({
            "request_id": f"REQ-{1000 + i}",
            "department": department,
            "service_type": service_type,
            "request_date": request_date,
            "current_stage": current_stage,
            "assigned_officer": officer,
            "priority": priority,
            "sla_deadline": sla_deadline,
            "sla_hours": sla_hours,
            "hours_used": round(age_hours, 1),
            "sla_usage_pct": sla_pct,
            "status": status,
            "risk_score": score,
            "risk_level": level,
        })

    df = pd.DataFrame(rows)
    df["impact"] = df.apply(delay_impact_score, axis=1)
    return df
