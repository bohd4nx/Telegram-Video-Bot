from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.utils import process_video

router = Router(name=__name__)


@router.message(F.video)
async def video_handler(message: Message, i18n: I18nContext, bot: Bot) -> None:
    await process_video(message, i18n, bot)


@router.message(~F.video & ~Command("start") & ~Command("help"))
async def handle_unknown_input(message: Message, i18n: I18nContext) -> None:
    await message.delete()
    await message.answer(i18n.get("unknown-input-text"))
