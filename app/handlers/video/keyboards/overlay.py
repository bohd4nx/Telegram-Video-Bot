from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def overlay_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🤖 Android — прозрачный фон",
            icon_custom_emoji_id="5807792908094413296",
            callback_data="overlay:android",
        ),
        InlineKeyboardButton(
            text="🍎 iOS — белый фон",
            icon_custom_emoji_id="5807792908094413297",
            callback_data="overlay:ios",
        ),
    )
    return builder.as_markup()
