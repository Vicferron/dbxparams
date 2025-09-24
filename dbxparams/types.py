from datetime import datetime, date
from typing import Any, Type
from .errors import InvalidTypeError


def cast_value(value: Any, expected_type: Type, name: str = "") -> Any:
    """
    Convert a raw value (usually string from dbutils) into the expected type.

    Args:
        value: The raw input value.
        expected_type: The type to cast into.
        name: Optional parameter name, used for better error messages.

    Returns:
        The value converted into expected_type.

    Raises:
        InvalidTypeError: If conversion fails.
    """
    if value is None:
        return None

    # Already correct type
    if isinstance(value, expected_type):
        return value

    raw = str(value).strip()

    try:
        if expected_type is str:
            return raw

        if expected_type is int:
            return int(raw)

        if expected_type is float:
            return float(raw)

        if expected_type is bool:
            if raw.lower() in ("1", "true", "yes", "y"):
                return True
            if raw.lower() in ("0", "false", "no", "n"):
                return False
            raise ValueError("Invalid boolean value")

        if expected_type is date:
            return datetime.strptime(raw, "%Y-%m-%d").date()

        if expected_type is datetime:
            formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
            for fmt in formats:
                try:
                    return datetime.strptime(raw, fmt)
                except ValueError:
                    continue
            raise ValueError("Invalid datetime format")

        # Fallback: try direct casting
        return expected_type(raw)

    except Exception:
        raise InvalidTypeError(name, expected_type, raw)
