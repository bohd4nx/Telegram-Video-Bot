import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from app.core import logger, setup_logging, config
from app.handlers import router


async def main() -> None:
    setup_logging()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )

    commands = [
        BotCommand(command="start", description="🚀 Start the app"),
        BotCommand(command="help", description="📖 Show help information")
    ]
    await bot.set_my_commands(commands)

    i18n_core = FluentRuntimeCore(path="locales/{locale}/LC_MESSAGES")
    await i18n_core.startup()
    logger.info(f"Loaded locales: {i18n_core.available_locales}")
    i18n = I18nMiddleware(core=i18n_core, default_locale="en")

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    i18n.setup(dispatcher=dp)

    try:
        await dp.start_polling(
            bot,
            polling_timeout=30,
            handle_as_tasks=True,
            tasks_concurrency_limit=100,
            close_bot_session=True,
        )
    finally:
        await i18n.core.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
