import logging
import os

import opik
from dotenv import load_dotenv


def configure_all():
    load_dotenv(override=True)
    configure_logger()
    configure_observability()


def configure_logger():
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()]
    )

def configure_observability():
    opik.configure(
        api_key=os.getenv("OPIK_API_KEY")
    )