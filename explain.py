"""Explainable AI (Module 3) — turns a risk score into plain-language reasons."""

from .constants import STAGE_DELAY_HISTORY, DEPARTMENT_DELAY_HISTORY


def explain_risk(row) -> list:
    reasons = []

    if row["sla_usage_pct"] >= 60:
        reasons.append(f"{row['sla_usage_pct']:.0f}% of the SLA time has been consumed.")

    stage_pct = STAGE_DELAY_HISTORY.get(row["current_stage"], 0)
    if stage_pct >= 40:
        reasons.append(
            f"The {row['current_stage']} stage historically delays {stage_pct}% of requests."
        )

    dept_pct = DEPARTMENT_DELAY_HISTORY.get(row["department"], 0)
    if dept_pct >= 50:
        reasons.append(f"{row['department']} department backlog detected ({dept_pct}% delay rate).")

    if row["priority"] == "High":
        reasons.append("Request is flagged High priority, raising its risk weighting.")

    if not reasons:
        reasons.append("Request is progressing within normal SLA parameters.")

    return reasons


def case_summary(row) -> str:
    """Bonus Feature: AI Case Summary — a one-paragraph narrative."""
    reasons = explain_risk(row)
    reason_text = " and ".join(reasons[:2]).lower() if len(reasons) > 1 else reasons[0].lower()
    return (
        f"Request {row['request_id']} is {row['risk_level'].lower()} risk "
        f"({row['risk_score']:.0f}/100), primarily because {reason_text} "
        f"{'Immediate escalation is recommended.' if row['risk_level'] == 'High' else 'Continued monitoring is recommended.'}"
    )
