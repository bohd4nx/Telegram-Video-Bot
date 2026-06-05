import asyncio
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DownloadTask:
    def __init__(self, url: str) -> None:
        self.url = url
        self.result: Path | None = None
        self.error: Exception | None = None
        self._done = asyncio.Event()
        self._task: asyncio.Task[None] = asyncio.get_event_loop().create_task(self._run())

    async def _run(self) -> None:
        from app.services.download.url import download_url

        try:
            self.result = await download_url(self.url)
        except Exception as exc:
            self.error = exc
        finally:
            self._done.set()
            asyncio.get_event_loop().call_later(600, _tasks.pop, _key(self.url), None)

    async def wait(self, timeout: float = 120.0) -> None:
        try:
            await asyncio.wait_for(asyncio.shield(self._done.wait()), timeout=timeout)
        except asyncio.TimeoutError:
            pass


# url_key → DownloadTask, auto-cleaned after 10 minutes
_tasks: dict[str, DownloadTask] = {}


def _key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:16]


def start(url: str) -> str:
    """Kick off a background download. Returns the key to pass to get()."""
    key = _key(url)
    if key not in _tasks:
        _tasks[key] = DownloadTask(url)
    return key


def get(key: str) -> DownloadTask | None:
    return _tasks.get(key)
