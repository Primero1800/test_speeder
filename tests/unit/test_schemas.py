from app.pyd.schemas import RequestResult, SpeedReport


def test_request_result_success():
    result = RequestResult(
        index=1, duration_sec=0.5, bytes_downloaded=1024, success=True
    )
    assert result.index == 1
    assert result.success is True
    assert result.error is None


def test_request_result_failure():
    result = RequestResult(
        index=2, duration_sec=1.0, bytes_downloaded=0, success=False, error="timeout"
    )
    assert result.success is False
    assert result.error == "timeout"
    assert result.bytes_downloaded == 0


def test_speed_report():
    report = SpeedReport(
        url="https://example.com",
        total_requests=10,
        successful_requests=8,
        total_bytes=1048576,
        total_time_sec=4.0,
        avg_time_sec=0.5,
        speed_mbps=2.0,
    )
    assert report.url == "https://example.com"
    assert report.speed_mbps == 2.0
    assert report.successful_requests == 8
