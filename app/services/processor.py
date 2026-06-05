import logging
from pathlib import Path

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.types import FSInputFile, Message
from aiogram_i18n import I18nContext

from app.core.constants import VIDEO_OUTPUT_SIZE

from .errors import handle_errors
from .video.encode import encode_all_segments

logger = logging.getLogger(__name__)


async def process_and_send(
    source: Path,
    chat_id: int,
    original_msg_id: int,
    status_msg: Message,
    overlay: str,
    i18n: I18nContext,
    bot: Bot,
) -> None:
    files_to_delete = [source]

    try:
        segments = await encode_all_segments(source, chat_id, bot, overlay)
        files_to_delete.extend(path for path, _ in segments)

        for path, duration in segments:
            await bot.send_chat_action(
                chat_id=chat_id,
                action=ChatAction.UPLOAD_VIDEO_NOTE,
            )
            await bot.send_video_note(
                chat_id=chat_id,
                video_note=FSInputFile(path),
                duration=duration,
                length=VIDEO_OUTPUT_SIZE,
                reply_to_message_id=original_msg_id,
            )

        await status_msg.delete()

    except Exception as exc:
        await handle_errors(exc, source, status_msg, i18n)

    finally:
        for path in files_to_delete:
            path.unlink(missing_ok=True)
