from src.bot import constants
from src.bot.config import bot
from src.bot.jobs import send_task_reminder
from src.bot.utils import (
    new_uuid, from_now, edit_callback, delete_callback, info_callback
)

from src.scheduler import scheduler

from apscheduler.triggers.cron import CronTrigger

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=constants.START_RESPONSE)


@bot.message_handler(commands=["list"])
def list_tasks(message: Message) -> None:
    jobs = scheduler.get_jobs()
    if not jobs:
        bot.send_message(chat_id=message.chat.id, text=constants.NO_TASKS)
        return

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

    bot.send_message(
        chat_id=message.chat.id, text=constants.YOUR_TASKS, reply_markup=markup
    )


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
