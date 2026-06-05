import logging

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from .states import VideoState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(
    StateFilter(VideoState.waiting_overlay), F.data.startswith("overlay:")
)
async def overlay_chosen(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    bot: Bot,
) -> None:
    if not isinstance(callback.message, Message) or callback.data is None:
        return
    overlay = callback.data.split(":")[1]  # "android" | "ios"
    data = await state.get_data()
    await state.clear()

    await callback.message.delete()

    original_message = await bot.forward_message(
        chat_id=callback.message.chat.id,
        from_chat_id=callback.message.chat.id,
        message_id=data["video_message_id"],
    )

    await process_video(original_message, i18n, bot, overlay=overlay)


async def process_video(
    message: Message, i18n: I18nContext, bot: Bot, overlay: str = "ios"
) -> None:
    logger.info(
        "Processing video with overlay=%s for chat %s", overlay, message.chat.id
    )
    # TODO: implement actual video processing with overlay param
    await message.answer(i18n.get("processing-text"))
