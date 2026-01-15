from pathlib import Path

import ffmpeg


def build_filters(input_video: ffmpeg.nodes.FilterableStream, files_dir: Path) -> ffmpeg.nodes.FilterNode:
    overlay = ffmpeg.input(str(files_dir / "overlay.mov"), stream_loop=-1)

    cropped = (
        input_video.video
        .filter("crop", "min(in_w,in_h)", "min(in_w,in_h)", "(in_w-min(in_w,in_h))/2", "(in_h-min(in_w,in_h))/2")
        .filter("scale", 640, 640, flags="lanczos")
        .filter("setsar", "1/1")
        .filter("format", "yuva420p")
    )

    return ffmpeg.filter([cropped, overlay.video], "overlay", 0, 0, shortest=1)
