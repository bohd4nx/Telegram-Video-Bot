import logging

from aiogram import Bot, Router
from aiogram.enums import ChatAction
from aiogram.types import ChosenInlineResult, FSInputFile, InputMediaVideo
from aiogram_i18n import I18nContext

from app.services.download.cache import get as get_task
from app.services.errors import DownloadError, FileTooLargeError

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.chosen_inline_result()
async def chosen_result_handler(result: ChosenInlineResult, bot: Bot, i18n: I18nContext) -> None:
    inline_msg_id = result.inline_message_id
    if not inline_msg_id:
        return

    key = result.result_id
    dt = get_task(key)
    if dt is None:
        await bot.edit_message_text(
            inline_message_id=inline_msg_id,
            text=i18n.get("error-link-download"),
        )
        return

    # Wait for the download that was started in query handler
    await bot.edit_message_text(
        inline_message_id=inline_msg_id,
        text=i18n.get("link-downloading"),
    )
    await dt.wait(timeout=120.0)

    if dt.error is not None:
        if isinstance(dt.error, FileTooLargeError):
            await bot.edit_message_text(
                inline_message_id=inline_msg_id,
                text=i18n.get("error-file-too-large", size=dt.error.size_mb),
            )
        elif isinstance(dt.error, DownloadError):
            await bot.edit_message_text(
                inline_message_id=inline_msg_id,
                text=i18n.get("error-link-download"),
            )
        else:
            logger.exception("Inline download error", exc_info=dt.error)
            await bot.edit_message_text(
                inline_message_id=inline_msg_id,
                text=i18n.get("error-processing"),
            )
        return

    source = dt.result
    if source is None or not source.exists():
        await bot.edit_message_text(
            inline_message_id=inline_msg_id,
            text=i18n.get("error-processing"),
        )
        return

    try:
        # Upload to Telegram via sender's DM to get a file_id, then edit inline msg
        user_id = result.from_user.id
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_VIDEO)

        tmp_msg = await bot.send_video(
            chat_id=user_id,
            video=FSInputFile(source),
            disable_notification=True,
        )
        if tmp_msg.video is None:
            raise RuntimeError("No video in sent message")

        file_id = tmp_msg.video.file_id
        await tmp_msg.delete()

        await bot.edit_message_media(
            inline_message_id=inline_msg_id,
            media=InputMediaVideo(media=file_id),
        )

    except Exception:
        logger.exception("Failed to deliver inline video")
        await bot.edit_message_text(
            inline_message_id=inline_msg_id,
            text=i18n.get("error-processing"),
        )
    finally:
        source.unlink(missing_ok=True)
