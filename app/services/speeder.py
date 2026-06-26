import time

import aiohttp

from app.pyd.schemas import RequestResult, SpeedReport

_LINE = "━" * 54
_SEP = "─" * 52


class SpeedTesterService:
    """Runs sequential HTTP requests and reports download speed."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        count: int,
        timeout: int,
    ) -> None:
        self._session = session
        self._url = url
        self._count = count
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    async def run(self) -> SpeedReport:
        """Execute all requests sequentially and return the speed report."""
        self._print_header()
        results: list[RequestResult] = []

        for i in range(1, self._count + 1):
            result = await self._single_request(i)
            results.append(result)
            self._print_result(result)

        report = self._build_report(results)
        self._print_report(report)
        return report

    async def _single_request(self, index: int) -> RequestResult:
        start = time.monotonic()
        try:
            async with self._session.get(self._url, timeout=self._timeout) as response:
                content = await response.read()
            duration = time.monotonic() - start
            return RequestResult(
                index=index,
                duration_sec=round(duration, 3),
                bytes_downloaded=len(content),
                success=True,
            )
        except Exception as exc:
            duration = time.monotonic() - start
            return RequestResult(
                index=index,
                duration_sec=round(duration, 3),
                bytes_downloaded=0,
                success=False,
                error=str(exc),
            )

    def _build_report(self, results: list[RequestResult]) -> SpeedReport:
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

    def _print_header(self) -> None:
        print(f"\n{_LINE}")
        print("  INTERNET SPEED TEST")
        print(_LINE)
        print(f"  Target   : {self._url}")
        print(f"  Requests : {self._count}")
        print(_LINE)

    def _print_result(self, r: RequestResult) -> None:
        tag = f"{r.index:02d}/{self._count:02d}"
        if r.success:
            mb = r.bytes_downloaded / 1024 / 1024
            print(f"  [{tag}]  {r.duration_sec:.3f}s   {mb:.2f} MB  ✓")
        else:
            print(f"  [{tag}]  {r.duration_sec:.3f}s   ERROR: {r.error}  ✗")

    def _print_report(self, report: SpeedReport) -> None:
        mb_total = report.total_bytes / 1024 / 1024
        print(_LINE)
        print("  RESULTS")
        print(f"  {_SEP}")
        print(
            f"  Requests  : {report.successful_requests} / {report.total_requests} successful"
        )
        print(f"  Total data: {mb_total:.2f} MB")
        print(f"  Total time: {report.total_time_sec:.2f} s")
        print(f"  Avg time  : {report.avg_time_sec:.3f} s / request")
        print(f"  Speed     : ★  {report.speed_mbps:.2f} MB/s")
        print(f"{_LINE}\n")
