import re

# Locale settings
DEFAULT_LOCALE = "ru"
SUPPORTED_LOCALES = {"en", "ru"}

# File size limits
MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB
MAX_FILE_SIZE_MB = MAX_FILE_SIZE_BYTES / (1024 * 1024)

# Video processing parameters
SEGMENT_DURATION = 60.0  # seconds
VIDEO_OUTPUT_SIZE = 640  # px (Telegram video_note requirement)

# Supported URL pattern for link processing
URL_PATTERN = re.compile(
    r"https?://"
    r"(?:www\.|vm\.|vt\.)?"
    r"(?:tiktok\.com|instagram\.com|youtube\.com/shorts|youtu\.be)"
    r"[^\s]*",
    re.IGNORECASE,
)
