import logging
import tempfile
from pathlib import Path

import ffmpeg
from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramEntityTooLarge,
    TelegramForbiddenError,
)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_i18n import I18nContext

from app.services.encode import encode_segment

from .states import VideoState

logger = logging.getLogger(__name__)
router = Router(name=__name__)

_FILES_DIR = Path(__file__).resolve().parents[3] / "files"
_SEGMENT_DURATION = 60.0


@router.callback_query(StateFilter(VideoState.waiting_overlay), F.data.startswith("overlay:"))
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

    # Replace the overlay-choice bubble with a progress indicator in-place
    await callback.message.edit_text(i18n.get("processing"), reply_markup=None)

    await process_video(
        chat_id=callback.message.chat.id,
        original_msg_id=data["video_message_id"],
        file_id=data["video_file_id"],
        file_size=data["video_file_size"],
        status_msg=callback.message,
        i18n=i18n,
        bot=bot,
        overlay=overlay,
    )


async def process_video(
    chat_id: int,
    original_msg_id: int,
    file_id: str,
    file_size: int,
    status_msg: Message,
    i18n: I18nContext,
    bot: Bot,
    overlay: str = "ios",
) -> None:
    file_size_mb = round(file_size / (1024 * 1024), 1)
    source: Path | None = None
    encoded: list[tuple[Path, int]] = []

    try:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VIDEO_NOTE)
        source = await _download_video(file_id, bot)
        encoded = await _encode_all_segments(source, chat_id, bot, overlay)

        for seg_path, seg_duration in encoded:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO_NOTE)
            await bot.send_video_note(
                chat_id=chat_id,
                video_note=FSInputFile(seg_path),
                duration=seg_duration,
                length=640,
                reply_to_message_id=original_msg_id,
            )

        await status_msg.delete()

    except TelegramEntityTooLarge:
        await status_msg.edit_text(i18n.get("error-file-too-large", size=file_size_mb))
    except TelegramBadRequest as e:
        if "file is too big" in str(e).lower():
            await status_msg.edit_text(i18n.get("error-file-too-large", size=file_size_mb))
        else:
            await status_msg.edit_text(i18n.get("error-processing", error=str(e)))
    except TelegramForbiddenError as e:
        if "VOICE_MESSAGES_FORBIDDEN" in str(e):
            await status_msg.edit_text(i18n.get("voice-disabled"))
        else:
            await status_msg.edit_text(i18n.get("error-processing", error=str(e)))
    except Exception as e:
        logger.exception("Unexpected error while processing video")
        await status_msg.edit_text(i18n.get("error-processing", error=str(e)))
    finally:
        for seg_path, _ in encoded:
            seg_path.unlink(missing_ok=True)
        if source:
            source.unlink(missing_ok=True)


async def _download_video(file_id: str, bot: Bot) -> Path:
    file = await bot.get_file(file_id)
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        path = Path(f.name)
    await bot.download_file(file.file_path, path)  # type: ignore[arg-type]
    return path


async def _encode_all_segments(
    source: Path,
    chat_id: int,
    bot: Bot,
    overlay: str,
) -> list[tuple[Path, int]]:
    total = float(ffmpeg.probe(str(source))["format"]["duration"])
    segments: list[tuple[Path, int]] = []
    start = 0.0

    while start < total:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO_NOTE)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            out_path = Path(f.name)

        seg_duration = encode_segment(
            source,
            out_path,
            start,
            min(_SEGMENT_DURATION, total - start),
            _FILES_DIR,
            overlay,
        )
        segments.append((out_path, seg_duration))
        start += _SEGMENT_DURATION

    return segments
