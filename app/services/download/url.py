import asyncio
import shutil
import tempfile
import time
from pathlib import Path

import yt_dlp

from app.core.constants import MAX_FILE_SIZE_BYTES, URL_PATTERN, YT_DLP_MIN_INTERVAL
from app.services.errors import DownloadError, FileTooLargeError


class URLDownloader:
    _FORMAT = "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best"

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._last_at = 0.0

    async def _throttle(self) -> None:
        async with self._lock:
            wait = self._last_at + YT_DLP_MIN_INTERVAL - time.monotonic()
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_at = time.monotonic()

    def _download_sync(self, url: str, out_dir: Path) -> Path:
        opts: dict[str, object] = {
            "outtmpl": str(out_dir / "video.%(ext)s"),
            "format": self._FORMAT,
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
        size = downloaded.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError(round(size / (1024 * 1024), 1))

        return downloaded

    async def download(self, url: str) -> Path:
        """Download video via yt-dlp. Returns standalone temp file. Caller must delete."""
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            await self._throttle()
            downloaded = await asyncio.to_thread(self._download_sync, url, tmp_dir)
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


_downloader = URLDownloader()


def extract_url(text: str) -> str | None:
    m = URL_PATTERN.search(text)
    return m.group(0) if m else None


async def download_url(url: str) -> Path:
    return await _downloader.download(url)
