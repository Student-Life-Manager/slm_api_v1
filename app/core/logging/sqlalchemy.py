import logging


def setup_sql_logging():
    logging.basicConfig()
    logger = logging.getLogger("sqlalchemy.engine")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("\n[%(asctime)s] \x1b[32;20m%(message)s\x1b[0m\n")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
