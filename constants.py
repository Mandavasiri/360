"""Shared constants for DelayGuard 360."""

STAGES = [
    "Submitted",
    "Verification",
    "Approval",
    "Inspection",
    "Documentation",
    "Completion",
]

# Historical delay rate (%) per workflow stage — how often requests get stuck here
STAGE_DELAY_HISTORY = {
    "Submitted": 8,
    "Verification": 28,
    "Approval": 70,
    "Inspection": 46,
    "Documentation": 31,
    "Completion": 4,
}

DEPARTMENTS = [
    "Revenue",
    "Municipal Services",
    "Public Works",
    "Health",
    "Education",
    "Licensing",
]

# Historical delay rate (%) per department
DEPARTMENT_DELAY_HISTORY = {
    "Revenue": 72,
    "Municipal Services": 55,
    "Public Works": 63,
    "Health": 39,
    "Education": 34,
    "Licensing": 48,
}

SERVICE_TYPES = {
    "Revenue": ["Property Tax Assessment", "Tax Refund", "Revenue Certificate"],
    "Municipal Services": ["Water Connection", "Trade License", "Waste Permit"],
    "Public Works": ["Road Repair Request", "Drainage Complaint", "Streetlight Fix"],
    "Health": ["Health Certificate", "Sanitation Inspection", "Food License"],
    "Education": ["School Transfer Certificate", "Scholarship Application", "Admission Verification"],
    "Licensing": ["Business License", "Building Permit", "Vendor License"],
}

OFFICERS = [
    "A. Rao", "S. Mehta", "K. Nair", "P. Iyer", "R. Sharma",
    "V. Krishnan", "N. Fernandes", "D. Kulkarni", "M. Reddy", "J. Thomas",
    "L. Bhatt", "T. George", "C. Pillai", "B. Joshi", "H. Menon",
]

PRIORITIES = ["Low", "Medium", "High"]
PRIORITY_WEIGHTS = [0.4, 0.4, 0.2]

# SLA allowance in hours, by priority
SLA_HOURS = {"High": 72, "Medium": 168, "Low": 336}

PRIORITY_IMPACT = {"High": 100, "Medium": 60, "Low": 30}

RISK_LOW_MAX = 40
RISK_MEDIUM_MAX = 70

ROLES = ["Admin", "Manager", "Employee", "Citizen"]
