from datetime import datetime


def format_datetime(dt):
    """
    Format datetime for display
    """
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M")


def get_time_period(dt):
    """
    Convert datetime to time period
    """
    hour = dt.hour

    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


def calculate_unplanned_ratio(records):
    """
    Calculate percentage of unplanned snacks
    """
    if not records:
        return 0

    total = len(records)
    unplanned = sum(1 for r in records if not r.planned)

    return round(unplanned / total, 2)


def generate_simple_message(label):
    """
    Generate user-friendly message
    """
    if label == "High Risk":
        return "Your recent eating pattern shows frequent unplanned snacks."
    elif label == "Medium Risk":
        return "Your eating pattern shows moderate risk."
    else:
        return "Your eating pattern looks balanced."