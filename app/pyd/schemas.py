from pydantic import BaseModel


class RequestResult(BaseModel):
    index: int
    duration_sec: float
    bytes_downloaded: int
    success: bool
    error: str | None = None


class SpeedReport(BaseModel):
    url: str
    total_requests: int
    successful_requests: int
    total_bytes: int
    total_time_sec: float
    avg_time_sec: float
    speed_mbps: float
