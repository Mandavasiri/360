import pandas as pd
import random


def get_data():
    departments = [
        "Revenue",
        "Transport",
        "Health",
        "Education",
        "Municipal",
        "Public Works"
    ]

    statuses = [
        "In Progress",
        "Completed",
        "Overdue"
    ]

    risk_levels = [
        "Low",
        "Medium",
        "High"
    ]

    data = []

    for i in range(50):
        data.append({
            "request_id": f"REQ-{1000 + i}",
            "department": random.choice(departments),
            "status": random.choice(statuses),
            "risk_level": random.choice(risk_levels),
            "risk_score": random.randint(10, 100)
        })

    return pd.DataFrame(data)
