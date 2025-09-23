import pytest
from dbxparams.errors import (
    MissingParameterError,
    InvalidTypeError,
    ValidationError,
)


def test_missing_parameter_error_message():
    """Check MissingParameterError has a clear, verbose message."""
    with pytest.raises(MissingParameterError) as exc_info:
        raise MissingParameterError("market")

    msg = str(exc_info.value)
    assert "Parameter 'market' is required" in msg
    assert "dbutils widget" in msg or "defaults" in msg or "class default" in msg


def test_invalid_type_error_message():
    """Check InvalidTypeError shows expected vs actual type."""
    with pytest.raises(InvalidTypeError) as exc_info:
        raise InvalidTypeError("threshold", float, "not-a-float")

    msg = str(exc_info.value)
    assert "Parameter 'threshold'" in msg
    assert "expected type float" in msg
    assert "value 'not-a-float'" in msg


def test_validation_error_message():
    """Check ValidationError message includes reason."""
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("date", "Invalid format, expected YYYY-MM-DD")

    msg = str(exc_info.value)
    assert "Parameter 'date'" in msg
    assert "Invalid format" in msg
