from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from .keyboards import overlay_keyboard
from .states import VideoState

router = Router(name=__name__)


@router.message(F.video)
async def video_received(
    message: Message, state: FSMContext, i18n: I18nContext
) -> None:
    await state.set_state(VideoState.waiting_overlay)
    await state.update_data(video_message_id=message.message_id)
    await message.answer(
        i18n.get("choose-overlay-text"),
        reply_markup=overlay_keyboard(),
    )
