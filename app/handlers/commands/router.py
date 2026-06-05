from aiogram import Router

from . import help, start

router = Router(name=__name__)
router.include_routers(
    help.router,
    start.router,
)
