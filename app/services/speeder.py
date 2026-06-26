import time

import aiohttp

from app.core.aiohttp_exception_handler import aiohttp_exception_handler
from app.pyd.schemas import RequestResult, SpeedReport
from app.services.reporter import SpeedReporter


class SpeedTesterService:
    """Runs sequential HTTP requests and builds the speed report."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        count: int,
        timeout: int,
        reporter: SpeedReporter | None = None,
    ) -> None:
        """Initialize the speed tester

        :param:
            session: the aiohttp client session to use for requests
            url: the target URL to download from
            count: number of sequential requests to perform
            timeout: per-request timeout in seconds
            reporter: output handler; defaults to SpeedReporter()
        """
        self._session = session
        self._reporter = reporter or SpeedReporter()
        self._url = url
        self._count = count
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    async def run(self) -> SpeedReport:
        """Execute all requests sequentially and return the speed report

        :returns:
            report: the aggregated SpeedReport with timing and throughput data
        """
        self._reporter.print_header(self._url, self._count)
        results: list[RequestResult] = []

        for i in range(1, self._count + 1):
            start = time.monotonic()
            try:
                content = await self._fetch()
                duration = round(time.monotonic() - start, 3)
                result = RequestResult(
                    index=i,
                    duration_sec=duration,
                    bytes_downloaded=len(content),
                    success=True,
                )
            except Exception as exc:
                duration = round(time.monotonic() - start, 3)
                result = RequestResult(
                    index=i,
                    duration_sec=duration,
                    bytes_downloaded=0,
                    success=False,
                    error=str(exc),
                )
            results.append(result)
            self._reporter.print_result(result, self._count)

        report = self._build_report(results)
        self._reporter.print_report(report)
        return report

    @aiohttp_exception_handler(is_raise=True)
    async def _fetch(self) -> bytes:
        """Download the target URL and return raw response bytes

        :returns:
            content: the raw response body

        :raise:
            ClientResponseError: on HTTP 4xx/5xx responses
            ClientConnectionError: on network-level failures
        """
        async with self._session.get(self._url, timeout=self._timeout) as response:
            return await response.read()

    def _build_report(self, results: list[RequestResult]) -> SpeedReport:
        """Build the aggregated speed report from individual request results

        :param:
            results: list of results from all requests

        :returns:
            report: the SpeedReport with totals, averages, and throughput
        """
        successful = [r for r in results if r.success]
        total_bytes = sum(r.bytes_downloaded for r in successful)
        total_time = sum(r.duration_sec for r in successful)
        avg_time = round(total_time / len(successful), 3) if successful else 0.0
        speed = (
            round((total_bytes / 1024 / 1024) / total_time, 3)
            if total_time > 0
            else 0.0
        )
        return SpeedReport(
            url=self._url,
            total_requests=self._count,
            successful_requests=len(successful),
            total_bytes=total_bytes,
            total_time_sec=round(total_time, 3),
            avg_time_sec=avg_time,
            speed_mbps=speed,
        )
