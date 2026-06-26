import argparse
import asyncio
import sys

from app.adapters.http_client import http_client
from app.common.logging import logger
from app.core.config import settings
from app.services.reporter import reporter
from app.services.speeder import SpeedTesterService
from app.utils.validators import check_reachable, is_valid_url


async def _resolve_url_interactive() -> str:
    while True:
        raw = input(
            "\nEnter URL to test (Ctrl+C — quit, Enter — use system default): "
        ).strip()

        candidate = raw if raw else settings.TARGET_URL

        if not candidate:
            logger.error("System URL is not configured. Please enter a URL.")
            continue

        if not is_valid_url(candidate):
            logger.error(f"Not a valid URL: {candidate!r}. Please try again.")
            continue

        if not raw:
            logger.info(f"Using system URL: {candidate}")

        logger.info("Checking URL reachability...")
        if not await check_reachable(
            http_client.session, candidate, settings.REQUEST_TIMEOUT
        ):
            logger.error(f"URL is not reachable: {candidate!r}. Please try again.")
            continue

        return candidate


async def main() -> None:
    parser = argparse.ArgumentParser(description="Internet speed tester")
    parser.add_argument("--url", type=str, default=None, help="URL to test")
    args = parser.parse_args()

    await http_client.start()
    try:
        if args.url:
            if not is_valid_url(args.url):
                logger.error(f"Invalid URL: {args.url!r}")
                sys.exit(1)
            logger.info("Checking URL reachability...")
            if not await check_reachable(
                http_client.session, args.url, settings.REQUEST_TIMEOUT
            ):
                logger.error(f"URL is not reachable: {args.url!r}")
                sys.exit(1)
            url = args.url
        else:
            url = await _resolve_url_interactive()

        service = SpeedTesterService(
            session=http_client.session,
            url=url,
            count=settings.REQUEST_COUNT,
            timeout=settings.REQUEST_TIMEOUT,
            reporter=reporter,
        )
        await service.run()
    finally:
        await http_client.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
