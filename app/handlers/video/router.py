from aiogram import Router

from . import menu, process

router = Router(name=__name__)
router.include_routers(
    menu.router,
    process.router,
)
