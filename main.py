import argparse
import asyncio
import sys

from app.adapters.http_client import http_client
from app.common.logging import logger
from app.core.config import settings
from app.services.speeder import SpeedTesterService
from app.utils.validators import is_valid_url


def resolve_url(system_url: str) -> str:
    """Interactively resolve the target URL from user input or system config."""
    while True:
        raw = input(
            "\nEnter URL to test (or press Enter to use system default): "
        ).strip()
        if raw:
            if is_valid_url(raw):
                return raw
            logger.error(f"Not a valid URL: {raw!r}. Please try again.")
        else:
            if system_url and is_valid_url(system_url):
                logger.info(f"Using system URL: {system_url}")
                return system_url
            logger.error("System URL is not configured. Please enter a URL.")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Internet speed tester")
    parser.add_argument("--url", type=str, default=None, help="URL to test")
    args = parser.parse_args()

    if args.url:
        if not is_valid_url(args.url):
            logger.error(f"Invalid URL: {args.url!r}")
            sys.exit(1)
        url = args.url
    else:
        url = resolve_url(settings.TARGET_URL)

    await http_client.start()
    try:
        service = SpeedTesterService(
            session=http_client.session,
            url=url,
            count=settings.REQUEST_COUNT,
            timeout=settings.REQUEST_TIMEOUT,
        )
        await service.run()
    finally:
        await http_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
