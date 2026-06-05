import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(~F.video & ~Command("start") & ~Command("help"))
async def handle_unknown_input(message: Message, i18n: I18nContext) -> None:
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.debug("Unknown input from user %s: %s", user_id, message.content_type)
    await message.delete()
    await message.answer(i18n.get("unknown-input-text"))
