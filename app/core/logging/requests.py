import logging.config

import yaml

from app.core.middleware import get_correlation_id, get_request_id


class AppFilter(object):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        record.request_id = get_request_id()
        return True


def setup_requests_logging():
    with open("logging.yaml", encoding="utf-8") as main_config_file:
        config = yaml.load(main_config_file, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] \x1b[33;20m%(message)s\x1b[0m")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


logger = logging.getLogger("uvicorn")
