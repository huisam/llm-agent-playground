import logging
import os

import opik
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
load_dotenv(override=True)


class LlmApiConfig:
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    GOOGLE_API_KEY: str = os.environ["GOOGLE_API_KEY"]


def configure_observability():
    opik.configure(
        api_key=os.environ["OPIK_API_KEY"]
    )
