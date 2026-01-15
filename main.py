import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from app.core import config, logger, setup_logging
from app.handlers import help_router, start_router, video_router


async def main() -> None:
    setup_logging()
    
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    try:
        logger.info("Starting Telegram Video Bot...")

        i18n_middleware = I18nMiddleware(
            core=FluentRuntimeCore(path="locales/{locale}"),
            default_locale="en"
        )
        i18n_middleware.setup(dispatcher=dp)

        dp.include_routers(start_router, help_router, video_router)

        commands = [
            BotCommand(command="start", description="🚀 Start the app"),
            BotCommand(command="help", description="📖 Show help information")
        ]
        await bot.set_my_commands(commands)

        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
