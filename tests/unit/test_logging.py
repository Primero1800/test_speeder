import logging

import pytest

from app.common.logging import BLUE, GREEN, RED, WHITE, YELLOW, ColorFormatter


@pytest.fixture
def formatter():
    return ColorFormatter("%(levelname)s %(message)s", "%Y-%m-%d")


def _make_record(level: int, msg: str = "test") -> logging.LogRecord:
    return logging.LogRecord(
        name="test", level=level, pathname="", lineno=0, msg=msg, args=(), exc_info=None
    )


def test_format_debug(formatter):
    record = _make_record(logging.DEBUG)
    result = formatter.format(record)
    assert YELLOW in result


def test_format_info(formatter):
    record = _make_record(logging.INFO)
    result = formatter.format(record)
    assert GREEN in result


def test_format_warning(formatter):
    record = _make_record(logging.WARNING)
    result = formatter.format(record)
    assert BLUE in result


def test_format_error(formatter):
    record = _make_record(logging.ERROR, "error occurred")
    result = formatter.format(record)
    assert RED in result


def test_format_critical(formatter):
    record = _make_record(logging.CRITICAL, "critical failure")
    result = formatter.format(record)
    assert RED in result


def test_format_unknown_level_uses_white(formatter):
    record = _make_record(logging.NOTSET)
    result = formatter.format(record)
    assert WHITE in result
