from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

# supported telegram language prefixes mapped to app locales.
LANGUAGES = {
    "en": {"locale_key": "lang-en", "prefixes": ["en"]},
    "ru": {"locale_key": "lang-ru", "prefixes": ["ru", "uk", "ua"]},
}
DEFAULT_LOCALE = "ru"


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext | None = data.get("i18n")
        user = data.get("event_from_user")

        if i18n and user:
            try:
                lang_code = user.language_code or DEFAULT_LOCALE
                code = (lang_code or "").lower()
                for lang, meta in LANGUAGES.items():
                    if any(code.startswith(prefix) for prefix in meta["prefixes"]):
                        detected_lang = lang
                        break
                else:
                    detected_lang = DEFAULT_LOCALE
                await i18n.set_locale(detected_lang)
            except Exception:
                pass

        return await handler(event, data)
