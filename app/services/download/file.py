import tempfile
from pathlib import Path

from aiogram import Bot


async def download_tg_video(file_id: str, bot: Bot) -> Path:
    """Download video from Telegram by file_id. Caller must delete."""
    tg_file = await bot.get_file(file_id)
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        path = Path(f.name)
    await bot.download_file(tg_file.file_path, path)  # type: ignore[arg-type]
    return path
