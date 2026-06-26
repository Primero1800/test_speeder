import pytest

from app.utils.validators import is_valid_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/file.jpg",
        "http://example.com",
        "https://upload.wikimedia.org/wikipedia/commons/file.jpg",
        "https://example.com/path/to/file?size=large",
    ],
)
def test_valid_url(url: str) -> None:
    assert is_valid_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "",
        "not-a-url",
        "example.com",
        "ftp://example.com",
        "//example.com",
        "just text",
        "123",
    ],
)
def test_invalid_url(url: str) -> None:
    assert is_valid_url(url) is False
