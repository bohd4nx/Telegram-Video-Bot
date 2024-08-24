from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from cfg import GIF_1, GIF_2, DEV, CHANNEL, ADMIN_ID
from data.database import add_user, statistics, errors_count


async def start(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    username = message.from_user.username or ""
    last_name = message.from_user.last_name or ""

    # Add user to the database if not exists
    add_user(user_id, f"@{username}", user_name, last_name)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="👨‍💻 DEV", url=DEV),
        InlineKeyboardButton(text="🔗 Channel", url=CHANNEL)
    )

    caption = (
        f"👋 Hello, *{user_name}*!\n\n"
        "👾 This bot will help you convert videos into video messages, just send it to me!\n\n"
        "🤖 Source: [GitHub Repository](https://github.com/bohd4nx/Telegram-Video-Bot)\n\n"
        "*Available Commands:*\n"
        "/start - Start bot.\n"
        # "/about - Learn more about me.\n"
        # "/donate - Support me.\n"
        "/help - Find out how it works.\n"
        # "/language - Change language. (In development)\n"
        "/feedback - Leave your feedback to the developer.\n"
    )

    await message.answer_animation(
        animation=GIF_1,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=markup
    )


async def help(message: types.Message):
    caption = (
        "*How to Prepare a Video:*\n\n"
        "There are three important rules to follow:\n\n"
        "1. The video must be *square*. _(optional)_\n"
        "2. The resolution must be *360p*.\n_(optional, but affects processing speed)_.\n"
        "3. The video should be no longer than *60 seconds*.\n\n"
        "_You can adjust these parameters in the menu just before sending the video._\n\n"
        "*What to do with the video message afterwards?*\n\n"
        "After receiving the video message, you can forward it without the 'forwarded from' tag. To do this:\n\n"
        "1. Select the video message.\n"
        "2. Choose 'Forward' and select the recipient from the list.\n"
        "3. In the opened dialog at the bottom, click on the 'Forward message' panel.\n"
        "4. Select 'Hide sender's name'.\n"
        "5. Send the message.\n\n"
        "*❗ Important:* The file size limit for messages is *20 MB*. Ensure your video does not exceed this limit to avoid issues."
    )

    await message.answer_animation(
        animation=GIF_2,
        caption=caption,
        parse_mode="Markdown"
        # reply_markup=markup
    )


async def db(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        total_users, total_usage = statistics()
        error_count = errors_count()
        await message.reply(f"👥 Total users: *{total_users}*\n"
                            f"👾 Total bot usages: *{total_usage}*\n"
                            f"❌ Total error logs: *{error_count}*\n"
                            f"🗃️ For more info, check: `data/database.db`",
                            parse_mode='Markdown')
    else:
        await message.reply("⛔️ Access denied.")
