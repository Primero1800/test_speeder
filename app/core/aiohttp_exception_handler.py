from functools import wraps
from typing import Any, Callable, TypeVar

from aiohttp import ClientConnectionError, ClientResponseError

from app.common.logging import logger

T = TypeVar("T", bound=Callable[..., Any])


def aiohttp_exception_handler(
    fallback: Any = None,
    is_raise: bool = True,
) -> Callable[[T], T]:
    """Decorator to handle aiohttp exceptions from external HTTP requests.

    :param:
        fallback: value to return when is_raise is False and an exception occurs
        is_raise: if True re-raises the exception after logging; if False returns fallback

    :returns:
        decorator: the wrapping decorator
    """

    def decorator(func: Any) -> Any:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except (ClientResponseError, ClientConnectionError) as exc:
                logger.warning(f"[{func.__name__}] HTTP error: {exc!r}")
                if is_raise:
                    raise
                return fallback
            except Exception as exc:
                logger.error(f"[{func.__name__}] Unexpected error: {exc!r}")
                if is_raise:
                    raise
                return fallback

        return wrapper

    return decorator
