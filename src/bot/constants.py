from telebot import formatting

CRON_FORMAT = formatting.hcode(
    "Input cron string according to the format or 'c' to cancel"
    "┌───────  minute (0–59)"
    "│ ┌───────  hour (0–23)"
    "│ │ ┌─────── day/month (1–31)"
    "│ │ │ ┌──────── month (1-12)"
    "│ │ │ │ ┌───────── day/week"
    "│ │ │ │ │    (0–6, sun-sat)"
    "│ │ │ │ │"
    "* * * * *"
)

INFO_TASK_PREFIX = "info_"
EDIT_TASK_PREFIX = "edit_"
DELETE_TASK_PREFIX = "delete_"

CANCEL_COMMAND = "c"

NO_BOT_TOKEN = "No Telegram bot token found in env"

START_RESPONSE = "Hello! Send me a task you want to be reminded of."
NO_TASKS = "You have no tasks scheduled."
TASK_CREATION_CANCELLED = "Task creation has been cancelled."
INVALID_CRON_FORMAT = "Invalid cron format. Please try again."
TASK_CREATED = "Your task has been added!"
YOUR_TASKS = "Your tasks:"
TASK_DELETED = "Task deleted!"
TASK_NOT_FOUND = "Task not found."
