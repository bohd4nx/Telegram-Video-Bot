import logging
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from app.services import process_and_send

from .states import LinkState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(StateFilter(LinkState.waiting_overlay), F.data.startswith("overlay:"))
async def overlay_chosen(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    bot: Bot,
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
