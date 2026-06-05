from aiogram import Router

from . import commands, links, unknown, video

router = Router(name=__name__)
router.include_routers(
    commands.router,
    video.router,
    links.router,
    unknown.router,
)
