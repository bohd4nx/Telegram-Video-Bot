from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.user import UserCreate, upsert_user

router = Router(name=__name__)


@router.message(Command("start"))
async def start_command(message: Message, i18n: I18nContext, session: AsyncSession) -> None:
    user = message.from_user
    if user:
        await upsert_user(session, UserCreate(user_id=user.id, username=user.username))
    name = user.first_name if user else ""
    await message.answer(i18n.get("start", name=escape(name)))
