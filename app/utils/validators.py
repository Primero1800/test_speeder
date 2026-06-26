import aiohttp
from pydantic import AnyHttpUrl, TypeAdapter, ValidationError

from app.core.aiohttp_exception_handler import aiohttp_exception_handler

_url_adapter: TypeAdapter[AnyHttpUrl] = TypeAdapter(AnyHttpUrl)


def is_valid_url(value: str) -> bool:
    """Check whether a string is a valid HTTP or HTTPS URL

    :param:
        value: the string to validate

    :returns:
        result: True if valid HTTP/HTTPS URL, False otherwise
    """
    try:
        _url_adapter.validate_python(value)
        return True
    except ValidationError:
        return False


@aiohttp_exception_handler(fallback=False, is_raise=False)
async def check_reachable(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
) -> bool:
    """Verify that a URL responds to a HEAD request

    :param:
        session: the aiohttp client session to use
        url: the target URL to probe
        timeout: request timeout in seconds

    :returns:
        result: True if the server responds with status < 400 or 405, False on any error
    """
    async with session.head(
        url,
        timeout=aiohttp.ClientTimeout(total=timeout),
        allow_redirects=True,
    ) as response:
        # 405 = HEAD not allowed, but server is alive
        return response.status == 405 or response.status < 400
