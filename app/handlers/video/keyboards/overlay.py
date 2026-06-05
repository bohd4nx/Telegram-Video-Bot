from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def overlay_keyboard(android_text: str, ios_text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=android_text,
                    custom_emoji_id="5819078828017849357",
                    callback_data="overlay:android",
                ),
                InlineKeyboardButton(
                    text=ios_text,
                    custom_emoji_id="5818920837645867167",
                    callback_data="overlay:ios",
                ),
            ]
        ]
    )
