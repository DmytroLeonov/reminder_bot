from src.bot.config import bot
from src.bot import constants
from telebot.types import Message

from src.bot.jobs import send_task_reminder
from src.scheduler import scheduler

from apscheduler.triggers.cron import CronTrigger

import uuid
from datetime import datetime


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello! Send me a task you want to be reminded of."
    )


@bot.message_handler(commands=["list"])
def list_tasks(message: Message) -> None:
    jobs = scheduler.get_jobs()
    if not jobs:
        bot.send_message(
            message.chat.id,
            "You have no tasks scheduled."
        )
        return

    job_list: list[str] = []

    for job in jobs:
        next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M")
        task_message = job.kwargs["task_message"]
        job_list.append(f"[{next_run_time}] - {task_message}")

    bot.send_message(
        chat_id=message.chat.id,
        text="\n".join(job_list)
    )


@bot.message_handler(func=lambda message: True)
def add_task(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=constants.CRON_FORMAT
    )
    bot.register_next_step_handler(
        message,
        callback=choose_time,
        task_message=message.text
    )


def choose_time(
    message: Message,
    *,
    task_message: str,
) -> None:
    crontab = message.text
    if crontab == "c":
        bot.send_message(
            message.chat.id,
            "Task creation has been cancelled."
        )
        return

    try:
        trigger = CronTrigger.from_crontab(crontab)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Invalid cron format. Please try again."
        )
        bot.register_next_step_handler(message, choose_time, task_message=task_message)
        return

    scheduler.add_job(
        func=send_task_reminder,
        trigger=trigger,
        kwargs={
            "chat_id": message.chat.id,
            "task_message": task_message
        },
        id=str(uuid.uuid4())
    )
    bot.send_message(
        message.chat.id,
        "Your task has been added!"
    )
