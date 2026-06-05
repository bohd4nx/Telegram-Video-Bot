import logging
from pathlib import Path

from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge, TelegramForbiddenError
from aiogram.types import Message
from aiogram_i18n import I18nContext

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    pass


class FileTooLargeError(DownloadError):
    def __init__(self, size_mb: float) -> None:
        self.size_mb = size_mb
        super().__init__(f"File too large: {size_mb} MB")


async def handle_errors(
    exc: Exception,
    source: Path,
    status_msg: Message,
    i18n: I18nContext,
) -> None:
    """Map Telegram exceptions to user-facing i18n messages."""
    if isinstance(exc, TelegramEntityTooLarge) or (
        isinstance(exc, TelegramBadRequest) and "file is too big" in str(exc).lower()
    ):
        size_mb = round(source.stat().st_size / (1024 * 1024), 1)
        await status_msg.edit_text(i18n.get("error-file-too-large", size=size_mb))

    elif isinstance(exc, TelegramForbiddenError) and "VOICE_MESSAGES_FORBIDDEN" in str(exc):
        await status_msg.edit_text(i18n.get("voice-disabled"))

    else:
        if not isinstance(exc, (TelegramBadRequest, TelegramForbiddenError)):
            logger.exception("Unexpected error in pipeline")
        await status_msg.edit_text(i18n.get("error-processing"))
