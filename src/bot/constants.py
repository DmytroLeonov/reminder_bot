from telebot import formatting

CRON_FORMAT = formatting.hcode(
    "Input cron string according to the format or 'c' to cancel\n"
    "┌───────  minute (0–59)\n"
    "│ ┌───────  hour (0–23)\n"
    "│ │ ┌─────── day/month (1–31)\n"
    "│ │ │ ┌───────── month\n"
    "│ │ │ │     (1-12, jan-dec)\n"
    "│ │ │ │ ┌───────── day/week\n"
    "│ │ │ │ │    (0–6, mon-sun)\n"
    "│ │ │ │ │\n"
    "* * * * *"
)

INFO_TASK_PREFIX = "info_"
EDIT_TASK_PREFIX = "edit_"
DELETE_TASK_PREFIX = "delete_"

LIST_CALLBACK = "list"

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
