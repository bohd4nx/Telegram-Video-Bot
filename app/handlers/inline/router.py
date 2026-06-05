from aiogram import Router

from . import chosen, query

router = Router(name=__name__)
router.include_routers(
    query.router,
    chosen.router,
)
