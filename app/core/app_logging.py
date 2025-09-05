import logging.config
import json
import pathlib


def setup_logging():
    config_file = pathlib.Path("app/core/logging_configs/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config=config)


logger = logging.getLogger("general_logger")
logger.setLevel(logging.DEBUG)
