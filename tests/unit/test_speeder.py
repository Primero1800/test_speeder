from unittest.mock import patch

import pytest

from app.pyd.schemas import RequestResult, SpeedReport
from app.services.reporter import SpeedReporter
from app.services.speeder import SpeedTesterService


@pytest.mark.asyncio
async def test_run_all_successful(mock_session, mock_response, capsys):
    mock_response.read.return_value = b"x" * (1024 * 1024)
    service = SpeedTesterService(
        session=mock_session, url="https://example.com", count=3, timeout=10
    )
    report = await service.run()
    assert report.total_requests == 3
    assert report.successful_requests == 3
    assert report.total_bytes == 3 * 1024 * 1024
    out = capsys.readouterr().out
    assert "INTERNET SPEED TEST" in out
    assert "RESULTS" in out


@pytest.mark.asyncio
async def test_run_all_failed(mock_session, capsys):
    service = SpeedTesterService(
        session=mock_session, url="https://example.com", count=2, timeout=10
    )
    with patch.object(service, "_fetch", side_effect=Exception("network error")):
        report = await service.run()
    assert report.successful_requests == 0
    assert report.speed_mbps == 0.0
    out = capsys.readouterr().out
    assert "N/A" in out
    assert "ERROR" in out


@pytest.mark.asyncio
async def test_run_mixed(mock_session, mock_response, capsys):
    mock_response.read.return_value = b"x" * 512
    service = SpeedTesterService(
        session=mock_session, url="https://example.com", count=3, timeout=10
    )
    call_count = 0

    async def _patched_fetch():
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise Exception("transient failure")
        return b"x" * 512

    with patch.object(service, "_fetch", side_effect=_patched_fetch):
        report = await service.run()
    assert report.successful_requests == 2
    assert report.total_requests == 3


def test_build_report_no_successful(mock_session):
    service = SpeedTesterService(
        session=mock_session, url="https://example.com", count=3, timeout=10
    )
    results = [
        RequestResult(
            index=i, duration_sec=1.0, bytes_downloaded=0, success=False, error="err"
        )
        for i in range(1, 4)
    ]
    report = service._build_report(results)
    assert report.successful_requests == 0
    assert report.avg_time_sec == 0.0
    assert report.speed_mbps == 0.0


def test_build_report_zero_time(mock_session):
    service = SpeedTesterService(
        session=mock_session, url="https://example.com", count=1, timeout=10
    )
    results = [
        RequestResult(index=1, duration_sec=0.0, bytes_downloaded=1024, success=True)
    ]
    report = service._build_report(results)
    assert report.speed_mbps == 0.0


def test_print_result_success(capsys):
    reporter = SpeedReporter()
    result = RequestResult(
        index=1, duration_sec=0.5, bytes_downloaded=1024 * 1024, success=True
    )
    reporter.print_result(result, total=5)
    out = capsys.readouterr().out
    assert "✓" in out
    assert "01/05" in out


def test_print_result_failure(capsys):
    reporter = SpeedReporter()
    result = RequestResult(
        index=2, duration_sec=1.0, bytes_downloaded=0, success=False, error="timeout"
    )
    reporter.print_result(result, total=5)
    out = capsys.readouterr().out
    assert "✗" in out
    assert "timeout" in out


def test_print_report_no_successful(capsys):
    reporter = SpeedReporter()
    report = SpeedReport(
        url="https://example.com",
        total_requests=3,
        successful_requests=0,
        total_bytes=0,
        total_time_sec=0.0,
        avg_time_sec=0.0,
        speed_mbps=0.0,
    )
    reporter.print_report(report)
    out = capsys.readouterr().out
    assert "N/A" in out
