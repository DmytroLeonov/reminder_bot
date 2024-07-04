import logging
import os

import telebot
from src.bot import constants

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError(constants.NO_BOT_TOKEN)
if not ADMIN_CHAT_ID:
    logger.warning(constants.ADMIN_CHAT_ID)

bot = telebot.TeleBot(TOKEN)
