from aiogram import Router

from . import commands, video, unknown

router = Router(name=__name__)
router.include_routers(
    commands.router,
    video.router,
    unknown.router,
)
