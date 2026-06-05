import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from app.core import config, logger, setup_logging
from app.handlers import router


async def build_dispatcher(bot: Bot) -> tuple[Dispatcher, I18nMiddleware]:
    i18n_core = FluentCompileCore(
        path=str(Path(__file__).parent / "locales" / "{locale}" / "LC_MESSAGES")
    )
    await i18n_core.startup()

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    i18n = I18nMiddleware(core=i18n_core, default_locale="en")
    i18n.setup(dispatcher=dp)

    @dp.startup()
    async def on_startup() -> None:
        commands = [
            BotCommand(command="start", description="🚀 Start the app"),
            BotCommand(command="help", description="📖 Show help information"),
        ]
        await bot.set_my_commands(commands)

    @dp.shutdown()
    async def on_shutdown() -> None:
        await i18n.core.shutdown()

    return dp, i18n


async def main() -> None:
    setup_logging()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    dp, _ = await build_dispatcher(bot)

    await dp.start_polling(
        bot,
        polling_timeout=30,
        handle_as_tasks=True,
        tasks_concurrency_limit=100,
        close_bot_session=True,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
