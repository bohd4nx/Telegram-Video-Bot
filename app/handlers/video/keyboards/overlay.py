from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_i18n import I18nContext


def overlay_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("btn-ios"),
                    icon_custom_emoji_id="5818920837645867167",
                    callback_data="overlay:ios",
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("btn-android"),
                    icon_custom_emoji_id="5819078828017849357",
                    callback_data="overlay:android",
                ),
            ],
        ]
    )
