import logging

from dotenv import load_dotenv


def configure_all():
    load_dotenv(override=True)
    configure_logger()


def configure_logger():
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()]
    )
