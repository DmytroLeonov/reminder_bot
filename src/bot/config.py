import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    raise ValueError('No Telegram bot token found in env')

bot = telebot.TeleBot(TOKEN)
