from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.adapters.http_client import HttpClient


def test_session_not_started_raises():
    client = HttpClient()
    with pytest.raises(RuntimeError, match="not started"):
        _ = client.session


@pytest.mark.asyncio
async def test_start_creates_session():
    client = HttpClient()
    with patch("app.adapters.http_client.aiohttp.ClientSession") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        await client.start()
        assert client._session is mock_instance


@pytest.mark.asyncio
async def test_stop_closes_session():
    client = HttpClient()
    mock_session = MagicMock()
    mock_session.close = AsyncMock()
    client._session = mock_session
    await client.stop()
    mock_session.close.assert_called_once()
    assert client._session is None


@pytest.mark.asyncio
async def test_stop_when_not_started():
    client = HttpClient()
    await client.stop()


@pytest.mark.asyncio
async def test_session_property_returns_session():
    client = HttpClient()
    mock_session = MagicMock()
    client._session = mock_session
    assert client.session is mock_session
