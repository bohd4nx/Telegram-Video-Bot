from aiogram import Router

from . import commands, inline, links, unknown, video

router = Router(name=__name__)
router.include_routers(
    commands.router,
    video.router,
    links.router,
    inline.router,
    unknown.router,
)
