import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from app.core.config import config
from app.handlers.help import register_help_handlers
from app.handlers.start import register_start_handlers
from app.handlers.video import register_video_handlers

logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] - %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    try:
        logger.info("Starting Telegram Video Bot...")

        i18n_middleware = I18nMiddleware(
            core=FluentRuntimeCore(path="locales/{locale}"),
            default_locale="en"
        )
        
        register_start_handlers(dp)
        register_help_handlers(dp)
        register_video_handlers(dp)
        
        i18n_middleware.setup(dispatcher=dp)


        commands = [
            types.BotCommand(command="start", description="🚀 Start the app"),
            types.BotCommand(command="help", description="📖 Show help information")
        ]
        await bot.set_my_commands(commands)

        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
