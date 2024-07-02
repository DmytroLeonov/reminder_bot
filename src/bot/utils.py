from datetime import datetime
from pytz import timezone
import uuid


def new_uuid() -> str:
    return str(uuid.uuid4())


def from_now(time: datetime) -> str:
    td = time - datetime.now(tz=timezone("Europe/Sofia"))
    seconds = td.seconds
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    years = days // 365

    if years > 0:
        return f"{years}y"
    if days > 0:
        return f"{days}d"
    if hours > 0:
        return f"{hours}h"
    if minutes > 0:
        return f"{minutes}m"
    return f"{seconds}s"


def info_callback(job_id: str) -> str:
    return f"info_{job_id}"


def edit_callback(job_id: str) -> str:
    return f"edit_{job_id}"


def delete_callback(job_id: str) -> str:
    return f"delete_{job_id}"
