"""Validation for incoming expense payloads."""
from datetime import datetime

REQUIRED_FIELDS = ["title", "amount", "category", "date"]


def validate_expense_payload(data):
    """Validate a raw request body for creating an expense.

    Returns (is_valid: bool, error_message: str | None).
    """
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return False, f"Missing required field(s): {', '.join(missing)}"

    title = data["title"]
    if not isinstance(title, str) or not title.strip():
        return False, "title must be a non-empty string"

    amount = data["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False, "amount must be a number"
    if amount <= 0:
        return False, "amount must be greater than 0"

    category = data["category"]
    if not isinstance(category, str) or not category.strip():
        return False, "category must be a non-empty string"

    date_str = data["date"]
    if not isinstance(date_str, str):
        return False, "date must be a string in YYYY-MM-DD format"
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False, "date must be in YYYY-MM-DD format"

    return True, None
