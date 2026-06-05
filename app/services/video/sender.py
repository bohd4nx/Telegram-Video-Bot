from pathlib import Path

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.types import FSInputFile


async def send_video_notes(
    bot: Bot,
    chat_id: int,
    reply_to_message_id: int,
    segments: list[tuple[Path, int]],
) -> None:
    for seg_path, seg_duration in segments:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO_NOTE)
        await bot.send_video_note(
            chat_id=chat_id,
            video_note=FSInputFile(seg_path),
            duration=seg_duration,
            length=640,
            reply_to_message_id=reply_to_message_id,
        )
