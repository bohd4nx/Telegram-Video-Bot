from aiogram import Router

from . import dispatch, menu

router = Router(name=__name__)
router.include_routers(
    menu.router,
    dispatch.router,
)
