"""
Example taken from 
https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/135_modern_logging/main.py

See youtube video associated with this code:
https://youtu.be/9L77QExPmI0
"""

import logging.config
import logging.handlers
import pathlib
from llm_agent.utils.text_utils import load_json_file


LOGGING_CONFIG_FILE = "llm_agent/logging_config/logging_settings.json"
logger = logging.getLogger("llm_agent")


def setup_logging():
    """
    Set up logging configuration.

    Reads the logging configuration from the 'default_settings.json' file,
    configures the logging module using the configuration, starts the queue
    handler listener if present, and registers a listener stop function to
    be called on program exit.

    Returns:
      logger: The root logger object.

    """
    config_file = pathlib.Path(LOGGING_CONFIG_FILE)
    config = load_json_file(config_file)

    logging.config.dictConfig(config)

    return logger


def main():
    """
    This is the main function that sets up logging and demonstrates logging functionality.
    """
    logger = setup_logging()
    logging.basicConfig(level="INFO")
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
