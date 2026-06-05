import logging
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.download import DownloadCreate, add_download
from app.services import process_and_send

from .states import LinkState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


def _content_type_from_url(url: str) -> str:
    u = url.lower()
    if "tiktok.com" in u:
        return "tiktok"
    if "instagram.com" in u:
        return "instagram"
    if "youtube.com" in u or "youtu.be" in u:
        return "youtube_shorts"
    return "url"


@router.callback_query(StateFilter(LinkState.waiting_overlay), F.data.startswith("overlay:"))
async def overlay_chosen(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    bot: Bot,
    session: AsyncSession,
) -> None:
    if not isinstance(callback.message, Message) or callback.data is None:
        return

    overlay = callback.data.split(":")[1]
    data = await state.get_data()
    await state.clear()

    await callback.message.edit_text(i18n.get("processing"), reply_markup=None)

    await process_and_send(
        source=Path(data["local_source"]),
        chat_id=callback.message.chat.id,
        original_msg_id=data["link_message_id"],
        status_msg=callback.message,
        overlay=overlay,
        i18n=i18n,
        bot=bot,
    )
    if callback.from_user:
        url = data.get("source_url", "")
        await add_download(
            session,
            DownloadCreate(
                user_id=callback.from_user.id,
                content_type=_content_type_from_url(url),
                content_id=url or None,
            ),
        )
