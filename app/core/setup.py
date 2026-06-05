from aiogram import Bot
from aiogram.types import BotCommand

COMMANDS: dict[str, list[BotCommand]] = {
    "en": [
        BotCommand(command="start", description="🚀 Start the app"),
        BotCommand(command="help", description="📖 Show help information"),
    ],
    "ru": [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="📖 Показать инструкцию"),
    ],
}

DESCRIPTIONS: dict[str, str] = {
    "en": (
        "Send me any video and I'll convert it into a round video message.\n\n"
        "Choose an overlay style — Android (transparent) or iOS (white) — "
        "and get your circle video in seconds 🎥"
    ),
    "ru": (
        "Отправь мне любое видео, и я конвертирую его в круглое видеосообщение.\n\n"
        "Выбери стиль оверлея — Android (прозрачный) или iOS (белый) — "
        "и получи кружочек за несколько секунд 🎥"
    ),
}

SHORT_DESCRIPTIONS: dict[str, str] = {
    "en": "Convert any video into a round Telegram video message 🎥",
    "ru": "Конвертирует видео в круглое видеосообщение Telegram 🎥",
}


async def setup_bot_profile(bot: Bot) -> None:
    for lang, cmds in COMMANDS.items():
        await bot.set_my_commands(cmds, language_code=lang)

    for lang, desc in DESCRIPTIONS.items():
        await bot.set_my_description(desc, language_code=lang)

    for lang, short_desc in SHORT_DESCRIPTIONS.items():
        await bot.set_my_short_description(short_desc, language_code=lang)
