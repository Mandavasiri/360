"""Recommendation Engine (Module 4) — rule-based preventive actions."""

from .constants import DEPARTMENT_DELAY_HISTORY


def recommend_actions(row) -> list:
    actions = []

    if row["risk_score"] > 80:
        actions.append("Escalate request to supervisor.")

    if DEPARTMENT_DELAY_HISTORY.get(row["department"], 0) >= 60:
        actions.append("Reassign officer — department is overloaded.")

    if row["sla_usage_pct"] >= 85:
        actions.append("Prioritize processing — SLA time nearly exhausted.")

    if row["risk_score"] > 60 and row["priority"] != "High":
        actions.append("Consider raising priority level.")

    if row["risk_score"] > 70:
        actions.append("Notify supervisor of elevated risk.")

    if not actions:
        actions.append("No action needed — continue normal processing.")

    return actions


def delay_impact_score(row) -> str:
    """Bonus Feature: Delay Impact Score — Low / Medium / High / Critical."""
    weight = row["risk_score"]
    if row["priority"] == "High":
        weight += 15
    if row["department"] in ("Revenue", "Public Works"):
        weight += 5

    if weight >= 95:
        return "Critical"
    if weight >= 75:
        return "High"
    if weight >= 45:
        return "Medium"
    return "Low"
