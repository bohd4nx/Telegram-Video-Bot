import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    BOT_TOKEN: str

    def __init__(self) -> None:
        self._load_config()
        self._setup_properties()
        self._validate_config()

    @staticmethod
    def _load_config() -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if not env_path.exists():
            logger.error("Missing .env file")
            sys.exit(1)
        load_dotenv(env_path)

    def _setup_properties(self) -> None:
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip()

    def _validate_config(self) -> None:
        if not self.BOT_TOKEN:
            logger.error("Missing required environment variable: BOT_TOKEN")
            sys.exit(1)


config = Config()
