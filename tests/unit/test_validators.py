from unittest.mock import MagicMock

import aiohttp
import pytest

from app.utils.validators import check_reachable, is_valid_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/file.jpg",
        "http://example.com",
        "https://upload.wikimedia.org/wikipedia/commons/file.jpg",
        "https://example.com/path/to/file?size=large",
    ],
)
def test_valid_url(url: str) -> None:
    assert is_valid_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "",
        "not-a-url",
        "example.com",
        "ftp://example.com",
        "//example.com",
        "just text",
        "123",
    ],
)
def test_invalid_url(url: str) -> None:
    assert is_valid_url(url) is False


@pytest.mark.asyncio
async def test_check_reachable_success(mock_session, mock_response):
    mock_response.status = 200
    result = await check_reachable(mock_session, "https://example.com", 10)
    assert result is True


@pytest.mark.asyncio
async def test_check_reachable_method_not_allowed(mock_session, mock_response):
    mock_response.status = 405
    result = await check_reachable(mock_session, "https://example.com", 10)
    assert result is True


@pytest.mark.asyncio
async def test_check_reachable_not_found(mock_session, mock_response):
    mock_response.status = 404
    result = await check_reachable(mock_session, "https://example.com", 10)
    assert result is False


@pytest.mark.asyncio
async def test_check_reachable_connection_error_returns_false():
    from aiohttp import ClientConnectionError

    session = MagicMock(spec=aiohttp.ClientSession)
    session.head.side_effect = ClientConnectionError()
    result = await check_reachable(session, "https://example.com", 10)
    assert result is False
