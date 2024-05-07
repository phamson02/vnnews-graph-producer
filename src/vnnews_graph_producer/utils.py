from datetime import datetime


def date_from_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d-%H-%M")


def date_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d-%H-%M")
