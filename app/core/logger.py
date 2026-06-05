import logging


def setup_logging() -> None:
    formatter = logging.Formatter(fmt="[%(asctime)s] - %(levelname)s: %(message)s", datefmt="%d.%m.%y %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler], force=True)

    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)


logger = logging.getLogger(__name__)
