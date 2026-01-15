from pathlib import Path

import ffmpeg

from app.utils.filters import build_filters


def encode_segment(in_path: Path, output_path: Path, start_time: float, duration: float, files_dir: Path) -> None:
    input_video = ffmpeg.input(str(in_path), ss=start_time, t=duration, hwaccel="auto")
    final_video = build_filters(input_video, files_dir)

    ffmpeg.output(
        final_video.filter("format", "yuv420p"), input_video.audio, str(output_path), # Unresolved attribute reference 'filter' for class 'FilterNode'
        vcodec="libx264", preset="fast", crf=20, pix_fmt="yuv420p",
        acodec="aac", audio_bitrate="128k", fpsmax=60, threads=0
    ).overwrite_output().run(capture_stdout=True, capture_stderr=True, quiet=True)
