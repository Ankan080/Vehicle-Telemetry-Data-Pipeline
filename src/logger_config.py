import logging
from src.config import LOG_FILE


def get_logger(name="vehicle_pipeline"):

    # Create logs directory
    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger