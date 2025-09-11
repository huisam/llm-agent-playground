import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger