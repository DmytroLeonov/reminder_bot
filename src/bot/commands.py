from datetime import datetime

from src.bot import constants
from src.bot.config import bot
from src.bot.jobs import send_task_reminder
from src.bot.utils import (
    new_uuid, generate_list_markup, get_crontab, inline_keyboard_delete_button
)

from src.scheduler import scheduler

from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from telebot import formatting
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=constants.START_RESPONSE)


@bot.message_handler(commands=["list"])
def list_tasks(message: Message) -> None:
    jobs = scheduler.get_jobs()
    if not jobs:
        bot.send_message(chat_id=message.chat.id, text=constants.NO_TASKS)
        return

    markup = generate_list_markup(jobs)
    bot.send_message(
        chat_id=message.chat.id, text=constants.YOUR_TASKS, reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda query: query.data.startswith(constants.DELETE_TASK_PREFIX)
)
def delete_task(query: CallbackQuery) -> None:
    job_id = query.data.split("_")[1]
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        pass
    finally:
        jobs = scheduler.get_jobs()
        if not jobs:
            bot.delete_message(
                chat_id=query.message.chat.id,
                message_id=query.message.id
            )
            return

    markup = generate_list_markup(jobs)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.id,
        reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda query: query.data.startswith(constants.INFO_TASK_PREFIX)
)
def task_info(query: CallbackQuery) -> None:
    job_id = query.data.split("_")[1]
    job = scheduler.get_job(job_id)
    if not job:
        bot.answer_callback_query(
            callback_query_id=query.id,
            text=constants.TASK_NOT_FOUND
        )
        return

    task_message = job.kwargs["task_message"]
    next_run_time = datetime.strftime(job.next_run_time, "%Y-%m-%d %H:%M")
    crontab = get_crontab(job.trigger)
    markup = InlineKeyboardMarkup(row_width=1)
    delete_button = inline_keyboard_delete_button(job_id)
    markup.add(delete_button)
    bot.send_message(
        chat_id=query.message.chat.id,
        text=(
            f"{task_message}\n"
            f"{formatting.hbold('Next run time')}: {next_run_time}\n"
            f"{formatting.hbold('Crontab')}: {crontab}"
        ),
        reply_markup=markup,
        parse_mode="HTML"
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
        trigger = CronTrigger.from_crontab(crontab, timezone=scheduler.timezone)
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
