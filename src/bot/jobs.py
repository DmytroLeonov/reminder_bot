from src.bot.config import bot


def send_task_reminder(*, chat_id: str | int, task_message: str) -> None:
    bot.send_message(chat_id, task_message)
