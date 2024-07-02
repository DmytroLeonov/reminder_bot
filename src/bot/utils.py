from datetime import datetime
from pytz import timezone
import uuid

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.job import Job


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


def generate_list_markup(jobs: list[Job]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    for job in jobs:
        time_left = from_now(job.next_run_time)
        task_message = job.kwargs["task_message"]
        text = f"{time_left}: {task_message}"
        task_button = InlineKeyboardButton(
            text=text, callback_data=info_callback(job.id)
        )
        edit_button = InlineKeyboardButton(
            text="✏️", callback_data=edit_callback(job.id)
        )
        delete_button = InlineKeyboardButton(
            text="❌", callback_data=delete_callback(job.id)
        )

        markup.row(task_button)
        markup.row(edit_button, delete_button)

    return markup
