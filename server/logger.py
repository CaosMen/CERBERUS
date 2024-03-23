import sys
import inspect

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
)


def print_log(type: str, message: str):
    """ Print a log message and insert it into the database """

    method_name = inspect.stack()[1].function
    method_line = inspect.stack()[1].lineno
    combined_message = f"[{method_name}:{method_line}] {message}"

    if type == "info":
        logger.info(combined_message)
    elif type == "warning":
        logger.warning(combined_message)
    elif type == "error":
        logger.error(combined_message)
