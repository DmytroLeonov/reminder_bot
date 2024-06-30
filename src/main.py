# Load environment variables before the modules that use them
from dotenv import load_dotenv
load_dotenv()

from src.bot import bot  # noqa: E402


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
