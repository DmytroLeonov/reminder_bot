from src.bot import constants
from src.bot.config import bot
from src.bot.jobs import send_task_reminder
from src.bot.utils import new_uuid

from src.scheduler import scheduler

from apscheduler.triggers.cron import CronTrigger

from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=constants.START_RESPONSE)


@bot.message_handler(commands=["list"])
def list_tasks(message: Message) -> None:
    jobs = scheduler.get_jobs()
    if not jobs:
        bot.send_message(chat_id=message.chat.id, text=constants.NO_TASKS)
        return

    job_list: list[str] = []

    for job in jobs:
        next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M")
        task_message = job.kwargs["task_message"]
        job_list.append(f"[{next_run_time}] - {task_message}")

    text = "\n".join(job_list)
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=lambda message: True)
def add_task(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id, text=constants.CRON_FORMAT, parse_mode="HTML"
    )
    bot.register_next_step_handler(
        message=message, callback=choose_time, task_message=message.text
    )


def choose_time(message: Message, *, task_message: str) -> None:
    crontab = message.text.lower()
    if crontab == constants.CANCEL_COMMAND:
        bot.send_message(
            chat_id=message.chat.id, text=constants.TASK_CREATION_CANCELLED
        )
        return

    try:
        trigger = CronTrigger.from_crontab(crontab)
    except ValueError:
        bot.send_message(
            chat_id=message.chat.id, text=constants.INVALID_CRON_FORMAT
        )
        bot.register_next_step_handler(
            message=message, callback=choose_time, task_message=task_message
        )
        return

    scheduler.add_job(
        func=send_task_reminder,
        trigger=trigger,
        kwargs={"chat_id": message.chat.id, "task_message": task_message},
        id=new_uuid()
    )
    bot.send_message(chat_id=message.chat.id, text=constants.TASK_CREATED)
