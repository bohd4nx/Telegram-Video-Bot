import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from .keyboards import overlay_keyboard
from .states import VideoState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(F.video)
async def video_received(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    if message.video is None:
        return

    user_id = message.from_user.id if message.from_user else "unknown"
    await state.set_state(VideoState.waiting_overlay)
    await state.update_data(
        video_message_id=message.message_id,
        video_file_id=message.video.file_id,
        video_file_size=message.video.file_size,
    )
    await message.answer(
        i18n.get("overlay-choose"),
        reply_markup=overlay_keyboard(
            android_text=i18n.get("btn-android"),
            ios_text=i18n.get("btn-ios"),
        ),
    )
