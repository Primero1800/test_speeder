import aiohttp


class HttpClient:
    """Single shared aiohttp session — created on startup, closed on exit."""

    def __init__(self) -> None:
        """Initialize with session set to None until start() is called"""
        self._session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        """Open the aiohttp session; must be called before accessing session"""
        self._session = aiohttp.ClientSession()

    async def stop(self) -> None:
        """Close the aiohttp session if open; safe to call when not started"""
        if self._session is not None:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """Active aiohttp session

        :returns:
            session: the open ClientSession instance

        :raise:
            RuntimeError: if start() was not called
        """
        if self._session is None:
            raise RuntimeError("HttpClient is not started")
        return self._session


http_client = HttpClient()
