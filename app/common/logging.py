import logging
import sys

from app.core.config import settings

WHITE = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"


class ColorFormatter(logging.Formatter):
    """Logging formatter that colorizes level names and error messages for terminal output"""

    _COLORS: dict[int, str] = {
        logging.DEBUG: YELLOW,
        logging.INFO: GREEN,
        logging.WARNING: BLUE,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Apply ANSI color codes to the log record and delegate to parent formatter

        :param:
            record: the log record to format

        :returns:
            formatted: the formatted log string with color codes applied
        """
        color = self._COLORS.get(record.levelno, WHITE)
        record.levelname = f"{color}{record.levelname}{WHITE}"
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            record.msg = f"{RED}{record.msg}{WHITE}"
        return super().format(record)


_FMT = "%(asctime)s [%(levelname)s] %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("speeder")
logger.propagate = False

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(ColorFormatter(_FMT, _DATEFMT))
logger.addHandler(_handler)
logger.setLevel(settings.LOG_LEVEL.upper())
