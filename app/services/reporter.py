from app.pyd.schemas import RequestResult, SpeedReport

_LINE = "━" * 54
_SEP = "─" * 52


class SpeedReporter:
    """Handles all console output for the speed test."""

    def print_header(self, url: str, count: int) -> None:
        """Print the test header with target URL and request count

        :param:
            url: the target URL being tested
            count: total number of requests to be made
        """
        print(f"\n{_LINE}")
        print("  INTERNET SPEED TEST")
        print(_LINE)
        print(f"  Target   : {url}")
        print(f"  Requests : {count}")
        print(_LINE)

    def print_result(self, r: RequestResult, total: int) -> None:
        """Print the result of a single request

        :param:
            r: the request result to display
            total: total number of requests (used for the progress tag)
        """
        tag = f"{r.index:02d}/{total:02d}"
        if r.success:
            mb = r.bytes_downloaded / 1024 / 1024
            print(f"  [{tag}]  {r.duration_sec:.3f}s   {mb:.2f} MB  ✓")
        else:
            print(f"  [{tag}]  {r.duration_sec:.3f}s   ERROR: {r.error}  ✗")

    def print_report(self, report: SpeedReport) -> None:
        """Print the final aggregated speed report

        :param:
            report: the completed SpeedReport to display
        """
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
        if report.successful_requests == 0:
            print("  Speed     : N/A — no successful requests")
        else:
            print(f"  Speed     : ★  {report.speed_mbps:.2f} MB/s")
        print(f"{_LINE}\n")


reporter = SpeedReporter()
