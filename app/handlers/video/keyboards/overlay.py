from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def overlay_keyboard(android_text: str, ios_text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=android_text,
                    callback_data="overlay:android",
                ),
                InlineKeyboardButton(
                    text=ios_text,
                    callback_data="overlay:ios",
                ),
            ]
        ]
    )
