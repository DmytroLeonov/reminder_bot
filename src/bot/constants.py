from telebot import formatting

CANCEL_COMMAND = "c"
CRON_FORMAT = formatting.hcode(
    f"Input cron string according to the format or '{CANCEL_COMMAND}' to cancel\n"
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

COMMAND_NOT_ALLOWED = "You are not allowed to use this command."

INFO_TASK_PREFIX = "info:"
DELETE_TASK_PREFIX = "delete:"
EDIT_TASK_MESSAGE_PREFIX = "edit_message:"
EDIT_TASK_CRON_PREFIX = "edit_cron:"

LIST_CALLBACK = "list"


NO_BOT_TOKEN = "No BOT_TOKEN found in env."
ADMIN_CHAT_ID = "No ADMIN_CHAT_ID found in env. You won't be able to use all features."

START_RESPONSE = "Hello! Send me a task you want to be reminded of."
NO_TASKS = "You have no tasks scheduled."
TASK_CREATION_CANCELLED = "Task creation has been cancelled."
INVALID_CRON_FORMAT = "Invalid cron format. Please try again."
TASK_CREATED = "Your task has been added!"
YOUR_TASKS = "Your tasks:"
TASK_DELETED = "Task deleted!"
TASK_NOT_FOUND = "Task not found."
