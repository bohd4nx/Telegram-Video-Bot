from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from cfg import ADMIN_ID
from data.database import save_feedback


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


async def feedback(message: types.Message):
    await message.reply("✉️ Please send your feedback message.\nSupported format is text only.\nType /cancel to exit.")
    await FeedbackState.waiting_for_feedback.set()


async def received(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.reply("❌ Unsupported format. Please send a text message only.")
        return

    user_id = message.from_user.id
    username = message.from_user.username or "None"
    user_message = message.text

    # Save feedback to the database
    save_feedback(user_id, username, user_message)

    # Send feedback to the admin
    feedback_text = f"🆕 *New Feedback from* @{username} || {user_id}\n\n*Message:* _{user_message}_"
    await message.bot.send_message(chat_id=ADMIN_ID, text=feedback_text, parse_mode="Markdown")

    await message.reply("❤️ Thank you for your feedback, the message has been forwarded to the developer.")

    await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    await message.reply("🤖 Feedback submission has been cancelled.")
    await state.finish()
