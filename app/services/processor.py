import logging
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message
from aiogram_i18n import I18nContext

from .errors import handle_errors
from .video.encode import encode_all_segments
from .video.sender import send_video_notes

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
    """
    Core pipeline: encode source → send video notes → cleanup.
    All Telegram errors are handled and mapped to i18n messages.
    """
    segments: list[tuple[Path, int]] = []
    try:
        segments = await encode_all_segments(source, chat_id, bot, overlay)
        await send_video_notes(bot, chat_id, original_msg_id, segments)
        await status_msg.delete()

    except Exception as exc:
        await handle_errors(exc, source, status_msg, i18n)

    finally:
        for seg_path, _ in segments:
            seg_path.unlink(missing_ok=True)
        source.unlink(missing_ok=True)
