import logging

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram_i18n import I18nContext

from app.services.download.cache import start as start_download
from app.services.download.url import extract_url

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.inline_query()
async def inline_query_handler(query: InlineQuery, i18n: I18nContext) -> None:
    text = (query.query or "").strip()
    url = extract_url(text)

    if not url:
        await query.answer(
            results=[],
            cache_time=1,
            is_personal=True,
        )
        return

    # Kick off background download immediately
    key = start_download(url)

    result = InlineQueryResultArticle(
        id=key,
        title=i18n.get("inline-as-video-title"),
        description=i18n.get("inline-as-video-desc"),
        input_message_content=InputTextMessageContent(
            message_text=i18n.get("link-downloading"),
        ),
    )

    await query.answer(results=[result], cache_time=5, is_personal=True)
