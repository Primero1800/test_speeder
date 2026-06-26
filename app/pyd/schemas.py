from pydantic import BaseModel


class RequestResult(BaseModel):
    """Result of a single HTTP request in the speed test"""

    index: int
    duration_sec: float
    bytes_downloaded: int
    success: bool
    error: str | None = None


class SpeedReport(BaseModel):
    """Aggregated report of all requests in a speed test run"""

    url: str
    total_requests: int
    successful_requests: int
    total_bytes: int
    total_time_sec: float
    avg_time_sec: float
    speed_mbps: float
