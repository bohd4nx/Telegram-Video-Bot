from aiogram import types, Dispatcher, F
from aiogram.filters import Command

from ..utils import process_video


async def handle_unknown_input(message: types.Message, i18n):
    await message.delete()
    await message.answer(i18n.get("unknown-input-text"))


def register_video_handlers(dp: Dispatcher):
    dp.message.register(process_video, F.video)
    dp.message.register(handle_unknown_input, ~F.video & ~Command("start") & ~Command("help"))
