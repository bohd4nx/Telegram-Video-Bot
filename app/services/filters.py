from pathlib import Path

import ffmpeg

_SIZE = 640
_CROP = "min(in_w,in_h)"
_CROP_X = "(in_w-min(in_w,in_h))/2"
_CROP_Y = "(in_h-min(in_w,in_h))/2"


def _crop_square(stream: ffmpeg.nodes.FilterableStream) -> ffmpeg.nodes.FilterableStream:
    return (
        stream.video.filter("crop", _CROP, _CROP, _CROP_X, _CROP_Y)
        .filter("scale", _SIZE, _SIZE, flags="lanczos")
        .filter("setsar", "1/1")
    )


def android_filters(
    src: ffmpeg.nodes.FilterableStream,
    files_dir: Path,
) -> ffmpeg.nodes.FilterableStream:
    plane = ffmpeg.input(str(files_dir / "plane.apng"), stream_loop=-1)
    circle_mask = ffmpeg.input(str(files_dir / "android.png"))

    # Crop to square, scale to 640 (keep -1 for blur bg, then scale up)
    base = src.video.filter("crop", _CROP, _CROP, _CROP_X, _CROP_Y).filter("scale", _SIZE, -1, flags="lanczos").split()

    # Background: tiny blur vignette
    background = (
        base[1]
        .filter("scale", 48, 48, flags="bilinear")
        .filter("eq", brightness=-0.25)
        .filter("gblur", sigma=3, steps=2)
        .filter("scale", _SIZE, _SIZE, flags="fast_bilinear")
    )

    foreground = ffmpeg.filter([base[0], circle_mask], "alphamerge")
    return background.overlay(plane, shortest=1).overlay(foreground)


def ios_filters(
    src: ffmpeg.nodes.FilterableStream,
    files_dir: Path,
) -> ffmpeg.nodes.FilterableStream:
    # Crop to square, apply circular alpha mask, composite on white background
    hole = ffmpeg.input(str(files_dir / "ios.png"))
    white_bg = ffmpeg.input(f"color=c=white:s={_SIZE}x{_SIZE}:r=60", f="lavfi")
    video = _crop_square(src)
    on_white = ffmpeg.filter([white_bg, video], "overlay", 0, 0, shortest=1)
    return ffmpeg.filter([on_white, hole], "overlay", 0, 0, shortest=1)


def build_filter_graph(
    src: ffmpeg.nodes.FilterableStream,
    files_dir: Path,
    overlay_type: str,
) -> ffmpeg.nodes.FilterableStream:
    if overlay_type == "ios":
        return ios_filters(src, files_dir)
    return android_filters(src, files_dir)
