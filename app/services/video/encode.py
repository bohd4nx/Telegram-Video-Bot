import logging
import tempfile
from pathlib import Path

import ffmpeg
from aiogram import Bot
from aiogram.enums import ChatAction

from app.core.constants import SEGMENT_DURATION
from app.services.video.filters import build_filter_graph

logger = logging.getLogger(__name__)

_FILES_DIR = Path(__file__).resolve().parents[3] / "files"

_VIDEO_OPTS: dict = dict(
    vcodec="libx264",
    preset="ultrafast",
    crf=20,
    pix_fmt="yuv420p",
    tune="zerolatency",
    movflags="+faststart",
    fpsmax=60,
    threads=0,
)
_AUDIO_OPTS: dict = dict(
    acodec="aac",
    audio_bitrate="128k",
)


def encode_segment(
    in_path: Path,
    out_path: Path,
    start: float,
    duration: float,
    overlay_type: str,
) -> int:
    src = ffmpeg.input(str(in_path), ss=start, t=duration, hwaccel="auto")
    video = build_filter_graph(src, _FILES_DIR, overlay_type).filter("format", "yuv420p")

    # Check whether the source has an audio stream
    probe = ffmpeg.probe(str(in_path))
    has_audio = any(s["codec_type"] == "audio" for s in probe.get("streams", []))

    streams = [video, src.audio] if has_audio else [video]
    opts = {**_VIDEO_OPTS, **({"acodec": "aac", "audio_bitrate": "128k"} if has_audio else {})}

    try:
        ffmpeg.output(
            *streams,
            str(out_path),
            **opts,
        ).overwrite_output().run(capture_stdout=True, capture_stderr=True, quiet=True)
    except ffmpeg.Error as e:
        logger.error("Error encoding segment: %s", e.stderr.decode() if e.stderr else "unknown error")
        raise

    return int(float(ffmpeg.probe(str(out_path))["format"]["duration"]))


async def encode_all_segments(
    source: Path,
    chat_id: int,
    bot: Bot,
    overlay: str,
) -> list[tuple[Path, int]]:
    total = float(ffmpeg.probe(str(source))["format"]["duration"])
    segments: list[tuple[Path, int]] = []
    start = 0.0

    while start < total:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VIDEO_NOTE)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            out_path = Path(f.name)

        seg_duration = encode_segment(
            source,
            out_path,
            start,
            min(SEGMENT_DURATION, total - start),
            overlay,
        )
        segments.append((out_path, seg_duration))
        start += SEGMENT_DURATION

    return segments
