from src.bot.config import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        "Hello! Send me a task you want to be reminded of."
    )


@bot.message_handler(func=lambda message: True)
def add_task(message: Message) -> None:
    bot.send_message(message.chat.id, message.text)
