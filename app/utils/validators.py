from pydantic import AnyHttpUrl, TypeAdapter, ValidationError

_url_adapter: TypeAdapter[AnyHttpUrl] = TypeAdapter(AnyHttpUrl)


def is_valid_url(value: str) -> bool:
    try:
        _url_adapter.validate_python(value)
        return True
    except ValidationError:
        return False
