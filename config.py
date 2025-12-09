import logging
import os
from typing import Any

import opik
from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("agent_app")


class Logger:
    @staticmethod
    def info(message: Any):
        logger.info(message)


def configure_observability():
    opik.configure(
        api_key=os.getenv("OPIK_API_KEY")
    )
