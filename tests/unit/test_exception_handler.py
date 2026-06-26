import pytest
from aiohttp import ClientConnectionError, ClientResponseError

from app.core.aiohttp_exception_handler import aiohttp_exception_handler


@pytest.mark.asyncio
async def test_success_returns_value():
    @aiohttp_exception_handler()
    async def func():
        return b"data"

    assert await func() == b"data"


@pytest.mark.asyncio
async def test_client_response_error_reraises():
    @aiohttp_exception_handler(is_raise=True)
    async def func():
        raise ClientResponseError(None, None)

    with pytest.raises(ClientResponseError):
        await func()


@pytest.mark.asyncio
async def test_client_connection_error_reraises():
    @aiohttp_exception_handler(is_raise=True)
    async def func():
        raise ClientConnectionError()

    with pytest.raises(ClientConnectionError):
        await func()


@pytest.mark.asyncio
async def test_unexpected_exception_reraises():
    @aiohttp_exception_handler(is_raise=True)
    async def func():
        raise ValueError("unexpected")

    with pytest.raises(ValueError):
        await func()


@pytest.mark.asyncio
async def test_is_raise_false_client_error_returns_fallback():
    @aiohttp_exception_handler(fallback="default", is_raise=False)
    async def func():
        raise ClientConnectionError()

    assert await func() == "default"


@pytest.mark.asyncio
async def test_is_raise_false_unexpected_returns_fallback():
    @aiohttp_exception_handler(fallback=None, is_raise=False)
    async def func():
        raise RuntimeError("unexpected")

    assert await func() is None
