from datetime import datetime, timezone


def validate_due_date_not_past(due_date: datetime) -> None:
    if due_date < datetime.now(timezone.utc):
        raise ValueError("due_date cannot be in the past")


def validate_non_empty_text(value: str) -> None:
    if value.strip() == "":
        raise ValueError("text cannot be empty")
