from aiogram import types, Dispatcher
from aiogram.filters import Command


async def start_command(message: types.Message, i18n):
    user = message.from_user
    text = i18n.get("start-text", name=user.first_name)
    await message.answer(text)


def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
