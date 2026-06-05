import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.keyboards import overlay_keyboard
from app.services.download import DownloadError, FileTooLargeError, download_url, extract_url

from .states import LinkState

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(F.text)
async def link_received(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    if not message.text:
        return

    url = extract_url(message.text)
    if url is None:
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
    )
    await message.reply(
        i18n.get("overlay-choose"),
        reply_markup=overlay_keyboard(i18n),
    )
