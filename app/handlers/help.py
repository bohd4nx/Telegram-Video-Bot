from aiogram import types, Dispatcher
from aiogram.filters import Command


async def help_command(message: types.Message, i18n):
    await message.delete()
    await message.answer(i18n.get("help-text"))


def register_help_handlers(dp: Dispatcher):
    dp.message.register(help_command, Command("help"))
