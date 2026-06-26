from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from app.services.speeder import SpeedTesterService


@pytest.fixture
def mock_response():
    resp = MagicMock()
    resp.read = AsyncMock(return_value=b"x" * 1024)
    resp.status = 200
    return resp


@pytest.fixture
def mock_session(mock_response):
    session = MagicMock(spec=aiohttp.ClientSession)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_response)
    cm.__aexit__ = AsyncMock(return_value=False)
    session.get.return_value = cm
    session.head.return_value = cm
    return session


@pytest.fixture
def make_speed_tester(mock_session):
    def factory(
        url: str = "https://example.com",
        count: int = 3,
        timeout: int = 10,
    ) -> SpeedTesterService:
        return SpeedTesterService(
            session=mock_session, url=url, count=count, timeout=timeout
        )

    return factory
