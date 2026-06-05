from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from app.core.constants import DEFAULT_LOCALE, SUPPORTED_LOCALES


def detect_locale(lang_code: str | None) -> str:
    locale = (lang_code or "").replace("_", "-").split("-")[0].lower()
    return locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext | None = data.get("i18n")
        user = data.get("event_from_user")

        if i18n is not None and user is not None:
            await i18n.set_locale(detect_locale(user.language_code))

        return await handler(event, data)
