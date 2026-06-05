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
    plane = ffmpeg.input(str(files_dir / "overlay.mov"), stream_loop=-1)
    circle_mask = ffmpeg.input(str(files_dir / "circle.png"))

    cropped = _crop_square(src).split()

    # Tiny downscale -> darken -> blur -> upscale = soft dark background vignette
    background = (
        cropped[1]
        .filter("scale", 48, 48, flags="bilinear")
        .filter("eq", brightness=-0.25)
        .filter("gblur", sigma=3, steps=2)
        .filter("scale", _SIZE, _SIZE, flags="fast_bilinear")
    )

    foreground = ffmpeg.filter([cropped[0], circle_mask], "alphamerge")
    with_plane = background.overlay(plane, shortest=1)
    return with_plane.overlay(foreground)


def ios_filters(
    src: ffmpeg.nodes.FilterableStream,
    files_dir: Path,
) -> ffmpeg.nodes.FilterableStream:
    # Crop to square, apply circular alpha mask, composite on white background
    video = (
        _crop_square(src)
        .filter("format", "rgba")
        .filter(
            "geq",
            r="r(X,Y)",
            g="g(X,Y)",
            b="b(X,Y)",
            a="if(lte(hypot(X-W/2,Y-H/2),W/2),255,0)",
        )
    )
    white_bg = ffmpeg.input(f"color=c=white:s={_SIZE}x{_SIZE}:r=60", f="lavfi")
    return ffmpeg.filter([white_bg, video], "overlay", 0, 0, shortest=1)


def build_filter_graph(
    src: ffmpeg.nodes.FilterableStream,
    files_dir: Path,
    overlay_type: str,
) -> ffmpeg.nodes.FilterableStream:
    if overlay_type == "ios":
        return ios_filters(src, files_dir)
    return android_filters(src, files_dir)
