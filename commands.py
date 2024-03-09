# commands.py
from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    start_message = (
        f"Hello, {user_name}!\n\n"
        "This is a bot designed to convert videos into video messages. "
        "Use /help for instructions.\n\n"
        "Administrator: @username\n"  # Replace with your username
        "Source: [GitHub](https://github.com/7GitGuru/Telegram-Video-Bot)"
    )
    await update.message.reply_text(start_message, parse_mode="Markdown", disable_web_page_preview=True)


async def help(update: Update, context: CallbackContext):
    help_message = (
        "<b>How to Prepare a Video: </b>\n\n"
        "There are three rules:\n"
        "1. The video must be <b>square</b>.\n"
        "2. Resolution must be <b>360p</b>.\n"
        "3. Not longer than <b>60 seconds</b>.\n\n"
        "You can adjust these parameters in the menu just before sending the video.\n\n"
        "<b>What to do with the video message afterwards?</b>\n\n"
        "You can forward the circle without the 'forwarded from' tag. To do this, select the circle -> "
        "Forward -> choose the recipient from the list -> "
        "in the opened dialog at the bottom, there will be a 'Forward message' panel, click on this panel -> "
        "select 'Hide sender's name' -> "
        "Send the message."
    )
    await update.message.reply_text(help_message, parse_mode="HTML")
