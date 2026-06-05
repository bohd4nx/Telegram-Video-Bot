import logging
from pathlib import Path

import ffmpeg

from app.services.filters import build_filter_graph

logger = logging.getLogger(__name__)

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
    files_dir: Path,
    overlay_type: str,
) -> int:
    src = ffmpeg.input(str(in_path), ss=start, t=duration, hwaccel="auto")
    video = build_filter_graph(src, files_dir, overlay_type).filter("format", "yuv420p")

    try:
        ffmpeg.output(
            video,
            src.audio,
            str(out_path),
            **_VIDEO_OPTS,
            **_AUDIO_OPTS,
        ).overwrite_output().run(capture_stdout=True, capture_stderr=True, quiet=True)
    except ffmpeg.Error as e:
        logger.error("Error encoding segment: %s", e.stderr.decode() if e.stderr else "unknown error")
        raise

    return int(float(ffmpeg.probe(str(out_path))["format"]["duration"]))
