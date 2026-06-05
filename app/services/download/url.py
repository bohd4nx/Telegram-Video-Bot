import asyncio
import logging
import shutil
import tempfile
from pathlib import Path

import yt_dlp

from app.core.constants import MAX_FILE_SIZE_BYTES, URL_PATTERN
from app.services.errors import DownloadError, FileTooLargeError

logger = logging.getLogger(__name__)

_YT_DLP_FORMAT = "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best"


def extract_url(text: str) -> str | None:
    m = URL_PATTERN.search(text)
    return m.group(0) if m else None


def _download_sync(url: str, out_dir: Path) -> Path:
    opts: dict[str, object] = {
        "outtmpl": str(out_dir / "video.%(ext)s"),
        "format": _YT_DLP_FORMAT,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
        ydl.download([url])

    files = list(out_dir.iterdir())
    if not files:
        raise DownloadError("Downloaded file not found")

    downloaded = files[0]
    size_mb = downloaded.stat().st_size / (1024 * 1024)
    if downloaded.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(round(size_mb, 1))

    return downloaded


async def download_url(url: str) -> Path:
    """Download video via yt-dlp. Returns standalone temp file. Caller must delete."""
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        downloaded = await asyncio.to_thread(_download_sync, url, tmp_dir)
        with tempfile.NamedTemporaryFile(suffix=downloaded.suffix, delete=False) as f:
            out_path = Path(f.name)
        shutil.move(str(downloaded), out_path)
        return out_path
    except (DownloadError, FileTooLargeError):
        raise
    except Exception as e:
        raise DownloadError(str(e)) from e
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
