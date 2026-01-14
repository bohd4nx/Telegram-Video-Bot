from app.handlers.help import router as help_router
from app.handlers.start import router as start_router
from app.handlers.video import router as video_router

__all__ = [
    'start_router',
    'help_router',
    'video_router'
]
