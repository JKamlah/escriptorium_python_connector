from datetime import datetime


def iso_string_date_to_datetime(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00").replace("z", "+00:00"))
