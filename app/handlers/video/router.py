from aiogram import Router

from . import menu

router = Router(name=__name__)
router.include_routers(
    menu.router,
)
