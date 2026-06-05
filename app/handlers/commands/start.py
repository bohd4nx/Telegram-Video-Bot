from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

router = Router(name=__name__)


@router.message(Command("start"))
async def start_command(message: Message, i18n: I18nContext) -> None:
    user = message.from_user
    text = i18n.get("start-text", name=user.first_name)
    await message.answer(text)
