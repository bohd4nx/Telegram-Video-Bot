import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import URL_DAILY_LIMIT
from app.database.download import count_url_downloads_today
from app.database.user import UserCreate, upsert_user
from app.keyboards import overlay_keyboard
from app.services.download import DownloadError, FileTooLargeError, download_url, extract_url

from .states import LinkState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(F.text)
async def link_received(message: Message, state: FSMContext, i18n: I18nContext, session: AsyncSession) -> None:
    if not message.text:
        return

    url = extract_url(message.text)
    if url is None:
        return

    if message.from_user:
        await upsert_user(session, UserCreate(user_id=message.from_user.id, username=message.from_user.username))
        count = await count_url_downloads_today(session, message.from_user.id)
        if count >= URL_DAILY_LIMIT:
            await message.reply(i18n.get("error-daily-limit", limit=URL_DAILY_LIMIT))
            return

    status = await message.reply(i18n.get("link-downloading"))

    try:
        source = await download_url(url)
    except FileTooLargeError as e:
        await status.edit_text(i18n.get("error-file-too-large", size=e.size_mb))
        return
    except DownloadError:
        logger.exception("Failed to download URL: %s", url)
        await status.edit_text(i18n.get("error-link-download"))
        return

    await status.delete()

    await state.set_state(LinkState.waiting_overlay)
    await state.update_data(
        link_message_id=message.message_id,
        local_source=str(source),
        source_url=url,
    )
    await message.reply(
        i18n.get("overlay-choose"),
        reply_markup=overlay_keyboard(i18n),
    )
