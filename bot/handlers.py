import os
from moviepy.editor import VideoFileClip
from aiogram.utils.exceptions import FileIsTooBig
from aiogram import types
from aiogram.types import InputFile
from cfg import STICKER, ADMIN_ID
from data.database import error, usage
from datetime import datetime


async def video(message: types.Message):
    bot = message.bot
    user_id = message.from_user.id
    username = message.from_user.username or "None"
    current_time = datetime.now().strftime("%H-%M-%S-%f")

    try:
        file_id = message.video.file_id
        file = await bot.get_file(file_id)

        # Check file size
        # if file.file_size > 20 * 1024 * 1024:  # 20 MB limit
        #     await message.reply("⚠️ The file is too large.\nPlease send a file smaller than 20 MB.")
        #     return

        processing_message = await message.reply_sticker(sticker=STICKER)

        # Create 'cache' directory if it doesn't exist
        temp_folder = "cache"
        os.makedirs(temp_folder, exist_ok=True)

        input_path = os.path.join(temp_folder, f"[{user_id}]_({current_time})_video.mp4")
        output_path = os.path.join(temp_folder, f"[{user_id}]_({current_time})_output_video.mp4")

        # Download video
        await bot.download_file(file.file_path, input_path)

        # Convert video
        input_video = VideoFileClip(input_path)
        w, h = input_video.size
        circle_size = 360
        aspect_ratio = float(w) / float(h)

        if w > h:
            new_w = int(circle_size * aspect_ratio)
            new_h = circle_size
        else:
            new_w = circle_size
            new_h = int(circle_size / aspect_ratio)

        resized_video = input_video.resize((new_w, new_h))
        output_video = resized_video.crop(
            x_center=resized_video.w / 2,
            y_center=resized_video.h / 2,
            width=circle_size,
            height=circle_size
        )
        output_video.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="5M")

        # Send video message
        video_note = InputFile(output_path, filename=f"{user_id}_{current_time}_output_video.mp4")
        await bot.send_video_note(chat_id=message.chat.id, video_note=video_note, duration=int(output_video.duration),
                                  length=circle_size)

        usage(user_id)

        # Cleanup
        os.remove(input_path)
        os.remove(output_path)

        # Delete processing message
        await processing_message.delete()

    except FileIsTooBig:
        await message.reply("⚠️ The file is too large.\nPlease send a file smaller than 20 MB.")
    except Exception as e:
        await message.reply("❌ An error occurred during processing. Please contact the developer.")
        error(user_id, username, str(e))
