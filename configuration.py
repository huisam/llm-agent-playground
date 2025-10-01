from dotenv import load_dotenv

from log.logger import configure_logger


def configure():
    load_dotenv(override=True)
    configure_logger()

