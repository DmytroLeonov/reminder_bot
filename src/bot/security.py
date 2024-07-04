from functools import wraps
import logging
import os

from telebot.types import Message

from src.bot.config import bot
from src.bot.constants import COMMAND_NOT_ALLOWED

logger = logging.getLogger(__name__)

ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID") or "-1")


def admin_only(func):
    @wraps(func)
    def wrapper(message: Message):
        if message.from_user.id != ADMIN_CHAT_ID:
            logger.warning(
                f"Attempt at unauthorized access in chat [{message.chat.id}]. "
                f"User: @{message.from_user.username} {message.from_user.full_name}. "
                f"Message: {message.text}."
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=COMMAND_NOT_ALLOWED
            )
            return
        func(message)
    return wrapper
