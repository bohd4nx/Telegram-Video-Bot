import tempfile
from pathlib import Path

import ffmpeg
from aiogram import Bot
from aiogram.exceptions import TelegramEntityTooLarge, TelegramForbiddenError
from aiogram.types import FSInputFile, Message
from aiogram_i18n import I18nContext


async def process_video(message: Message, i18n: I18nContext, bot: Bot):
    proc_msg = await message.reply(i18n.get("processing-text"))

    in_path = None
    overlay_path = Path(__file__).resolve().parents[2] / "files" / "overlay.mov"
    segment_paths = []

    # TODO: # replace built-in overlay, create mine, identical to Telegram's (with transparent background)

    try:
        file = await bot.get_file(message.video.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            in_path = Path(temp_file.name)

        await bot.download_file(file.file_path, in_path)

        probe_input = ffmpeg.probe(str(in_path))
        total_duration = float(probe_input["format"]["duration"])

        current_time = 0

        while current_time < total_duration:
            segment_duration = min(60.0, total_duration - current_time)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as output_file:
                output_path = Path(output_file.name)

                main_stream = ffmpeg.input(str(in_path), ss=current_time, t=segment_duration, hwaccel="auto")
                overlay_stream = ffmpeg.input(str(overlay_path), stream_loop=-1)

                main_video = (main_stream.video
                              .filter("crop", "min(in_w,in_h)", "min(in_w,in_h)", "(in_w-min(in_w,in_h))/2",
                                      "(in_h-min(in_w,in_h))/2")
                              .filter("scale", 640, -1, flags="lanczos")
                              .filter("format", "yuva420p"))

                video_with_overlay = ffmpeg.filter([main_video, overlay_stream.video], "overlay", x=0, y=0, shortest=1)

                (ffmpeg.output(
                    video_with_overlay.filter("format", "yuv420p"),
                    main_stream.audio,
                    str(output_path),
                    vcodec="libx264",
                    crf=25,
                    preset="ultrafast",
                    tune="fastdecode",
                    fpsmax=60,
                    acodec="aac",
                    audio_bitrate="96k",
                    format="mp4",
                    movflags="+faststart",
                    threads="0"
                ).overwrite_output().run(capture_stdout=True, capture_stderr=True, quiet=True))

            probe = ffmpeg.probe(str(output_path))
            actual_duration = int(float(probe["format"]["duration"]))
            segment_paths.append((output_path, actual_duration, 640))

            current_time += 60

        for seg_path, duration, size in segment_paths:
            await bot.send_video_note(
                chat_id=message.chat.id,
                video_note=FSInputFile(seg_path),
                duration=duration,
                length=size
            )

        await proc_msg.delete()

    except TelegramEntityTooLarge:
        await proc_msg.edit_text(i18n.get("file-too-large-text"))
    except TelegramForbiddenError as e:
        if "VOICE_MESSAGES_FORBIDDEN" in str(e):
            await proc_msg.edit_text(i18n.get("voice-messages-disabled-text"))
        else:
            await proc_msg.edit_text(i18n.get("processing-error-text", error=str(e)))
    except Exception as e:
        await proc_msg.edit_text(i18n.get("processing-error-text", error=str(e)))
    finally:
        for seg_path, _, _ in segment_paths:
            if seg_path.exists():
                seg_path.unlink()
        if in_path and in_path.exists():
            in_path.unlink()
