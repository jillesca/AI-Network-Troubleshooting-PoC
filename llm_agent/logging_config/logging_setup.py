"""
Example taken from 
https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/135_modern_logging/main.py

See youtube video associated with this code:
https://youtu.be/9L77QExPmI0
"""

import os
import pathlib
import logging.config
from llm_agent.utils.text_utils import load_json_file
from llm_agent.config.global_settings import (
    LOGGER_NAME,
    LOGGING_CONFIG_FILE,
)


def setup_logging():
    """
    Set up logging configuration.

    This function loads the logging configuration from a JSON file,
    ensures the log file exists, and configures the logging module.

    Returns:
      logger: The logger object.

    """
    config_file = pathlib.Path(LOGGING_CONFIG_FILE)
    config = load_json_file(config_file)

    log_file = _get_log_file_name(config)
    _ensure_log_file_exists(log_file)

    logging.config.dictConfig(config)

    return logging.getLogger(LOGGER_NAME)


def _ensure_log_file_exists(filename):
    """
    Ensures a log file exists. If it doesn't, creates it.

    Args:
      filename (str): The path and name of the log file.

    Returns:
      None
    """
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8"):
            pass


def _get_log_file_name(config):
    """
    Extracts the log file name from the configuration.

    Args:
      config (dict): The logging configuration.

    Returns:
      str: The log file name.
    """
    return config["handlers"]["file"]["filename"]


logger = setup_logging()


def main():
    """
    It sets up the logger and demonstrates logging at different levels.
    """
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
