from app.handlers.help import register_help_handlers
from app.handlers.start import register_start_handlers
from app.handlers.video import register_video_handlers

__all__ = [
    'register_start_handlers',
    'register_help_handlers',
    'register_video_handlers'
]
