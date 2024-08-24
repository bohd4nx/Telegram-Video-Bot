import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update, ContentType
from aiogram.utils import executor
from aiogram.contrib.middlewares.fsm import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.commands import start, help, db
from bot.feedback import received, feedback, cancel, FeedbackState
from bot.handlers import video
from cfg import TOKEN
from data.database import initialize_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.register_message_handler(start, commands=["start"])
dp.register_message_handler(help, commands=["help"])
dp.register_message_handler(db, commands=['db'])
dp.register_message_handler(feedback, commands="feedback", state="*")
dp.register_message_handler(cancel, commands="cancel", state=FeedbackState.waiting_for_feedback)
dp.register_message_handler(received, state=FeedbackState.waiting_for_feedback, content_types=ContentType.ANY)
dp.register_message_handler(video, content_types=["video"])

if __name__ == "__main__":
    initialize_db()
    executor.start_polling(dp, skip_updates=True)
