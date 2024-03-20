import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.commands import start, help
from bot.handlers import process_video

TOKEN = ""  # Replace with your token


def main():
    logging.basicConfig(level=logging.INFO)

    dp = Application.builder().token(TOKEN).build()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(filters.VIDEO, process_video))

    dp.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)


if __name__ == "__main__":
    main()
