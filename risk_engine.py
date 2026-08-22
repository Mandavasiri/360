"""AI Risk Prediction Engine (Module 2).

Risk Score = 40% SLA usage + 30% stage delay history
             + 20% department delay history + 10% priority impact
"""

from .constants import (
    STAGE_DELAY_HISTORY,
    DEPARTMENT_DELAY_HISTORY,
    PRIORITY_IMPACT,
    RISK_LOW_MAX,
    RISK_MEDIUM_MAX,
)


def sla_usage_pct(hours_used: float, sla_hours: float) -> float:
    if sla_hours <= 0:
        return 100.0
    return round(min(hours_used / sla_hours * 100, 100), 1)


def compute_risk_score(hours_used: float, sla_hours: float, stage: str,
                        department: str, priority: str) -> float:
    sla_pct = sla_usage_pct(hours_used, sla_hours)
    stage_pct = STAGE_DELAY_HISTORY.get(stage, 20)
    dept_pct = DEPARTMENT_DELAY_HISTORY.get(department, 40)
    pri_pct = PRIORITY_IMPACT.get(priority, 50)

    score = (0.40 * sla_pct) + (0.30 * stage_pct) + (0.20 * dept_pct) + (0.10 * pri_pct)
    return round(min(score, 100), 1)


def risk_level(score: float) -> str:
    if score <= RISK_LOW_MAX:
        return "Low"
    if score <= RISK_MEDIUM_MAX:
        return "Medium"
    return "High"


def risk_color(level: str) -> str:
    return {"Low": "#35D0A6", "Medium": "#F2A93B", "High": "#FF5C5C"}.get(level, "#8B98AC")


def simulate_recovery(current_score: float, extra_officers: int, priority_boost: bool) -> float:
    """Bonus Feature: SLA Recovery Simulator.

    Adding officers reduces department-load pressure; boosting priority reduces
    the SLA-usage pressure component. Simple, explainable heuristic reduction.
    """
    reduction = extra_officers * 9  # each extra officer eases ~9 risk points
    if priority_boost:
        reduction += 15
    new_score = max(current_score - reduction, 5)
    return round(new_score, 1)
