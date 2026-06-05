import logging

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DownloadCreate, add_download
from app.services import process_and_send
from app.services.download import download_tg_video

from .states import VideoState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(StateFilter(VideoState.waiting_overlay), F.data.startswith("overlay:"))
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

    source = await download_tg_video(data["video_file_id"], bot)
    await process_and_send(
        source=source,
        chat_id=callback.message.chat.id,
        original_msg_id=data["video_message_id"],
        status_msg=callback.message,
        overlay=overlay,
        i18n=i18n,
        bot=bot,
    )
    if callback.from_user:
        await add_download(
            session,
            DownloadCreate(
                user_id=callback.from_user.id,
                content_type="video_file",
                content_id=data["video_file_id"],
            ),
        )
