# handlers.py
import os

from moviepy.editor import VideoFileClip
from telegram import Update
from telegram.ext import CallbackContext


async def process_video(update: Update, context: CallbackContext):
    processing_message = await update.message.reply_text("❗️Processing...")

    video_file = await context.bot.get_file(update.message.video.file_id)

    # Creating 'temp' folder if it doesn't exist
    temp_folder = "temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    input_video_path = os.path.join(temp_folder, "input_video.mp4")
    output_video_path = os.path.join(temp_folder, "output_video.mp4")

    await video_file.download(input_video_path)

    # Convert
    input_video = VideoFileClip(input_video_path)
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
    output_video = resized_video.crop(x_center=resized_video.w / 2, y_center=resized_video.h / 2, width=circle_size,
                                      height=circle_size)
    output_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", bitrate="5M")

    # Send
    with open(output_video_path, "rb") as video:
        await context.bot.send_video_note(chat_id=update.message.chat_id, video_note=video,
                                          duration=int(output_video.duration), length=circle_size)

    # Delete
    os.remove(input_video_path)
    os.remove(output_video_path)

    # Delete message
    await processing_message.delete()
