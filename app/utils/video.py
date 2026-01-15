import logging
import tempfile
from pathlib import Path

import ffmpeg
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge, TelegramForbiddenError
from aiogram.types import FSInputFile, Message
from aiogram_i18n import I18nContext

from app.utils.encode import encode_segment

logger = logging.getLogger(__name__)


async def process_video(message: Message, i18n: I18nContext, bot: Bot) -> None:
    proc_msg = await message.reply(i18n.get("processing-text"))
    files_dir = Path(__file__).resolve().parents[2] / "files"
    in_path: Path | None = None
    segment_paths: list[tuple[Path, int, int]] = []
    file_size_mb = round(message.video.file_size / (1024 * 1024), 1)

    try:
        file = await bot.get_file(message.video.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            in_path = Path(temp_file.name)
        await bot.download_file(file.file_path, in_path)

        total_duration = float(ffmpeg.probe(str(in_path))["format"]["duration"])
        current_time = 0

        while current_time < total_duration:
            duration = min(60.0, total_duration - current_time)
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
                output_path = Path(f.name)

            try:
                encode_segment(in_path, output_path, current_time, duration, files_dir)
                actual_duration = int(float(ffmpeg.probe(str(output_path))["format"]["duration"]))
                segment_paths.append((output_path, actual_duration, 640))
            except ffmpeg.Error as e:
                logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else 'Unknown'}")
                raise

            current_time += 60

        for seg_path, duration, size in segment_paths:
            await bot.send_video_note(
                chat_id=message.chat.id,
                video_note=FSInputFile(seg_path),
                duration=duration,
                length=size
            )

        await proc_msg.delete()

    except TelegramEntityTooLarge:
        await proc_msg.edit_text(i18n.get("file-too-large-text", size=file_size_mb))
    except TelegramBadRequest as e:
        if "file is too big" in str(e).lower():
            await proc_msg.edit_text(i18n.get("file-too-large-text", size=file_size_mb))
        else:
            await proc_msg.edit_text(i18n.get("processing-error-text", error=str(e)))
    except TelegramForbiddenError as e:
        if "VOICE_MESSAGES_FORBIDDEN" in str(e):
            await proc_msg.edit_text(i18n.get("voice-messages-disabled-text"))
        else:
            await proc_msg.edit_text(i18n.get("processing-error-text", error=str(e)))
    except Exception as e:
        await proc_msg.edit_text(i18n.get("processing-error-text", error=str(e)))
    finally:
        for seg_path, _, _ in segment_paths:
            seg_path.unlink(missing_ok=True)
        if in_path:
            in_path.unlink(missing_ok=True)
