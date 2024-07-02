import telebot
from src.bot.constants import NO_BOT_TOKEN
import os

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError(NO_BOT_TOKEN)

bot = telebot.TeleBot(TOKEN)
