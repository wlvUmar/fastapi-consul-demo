import logging

import colorlog


def setup_logging(name: str) -> logging.Logger:
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(asctime)s %(blue)s%(name)s%(reset)s %(message)s"
        )
    )
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
