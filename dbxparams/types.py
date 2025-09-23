from datetime import datetime, date
from typing import Any, Type


def cast_value(value: Any, expected_type: Type) -> Any:
    """
    Convert a raw value (usually string from dbutils) into the expected type.

    Args:
        value: The raw input value.
        expected_type: The type to cast into.

    Returns:
        The value converted into expected_type.

    Raises:
        ValueError: If conversion fails.
    """
    if value is None:
        return None

    # Short-circuit: already correct type
    if isinstance(value, expected_type):
        return value

    # Normalize: dbutils always returns str
    raw = str(value).strip()

    if expected_type is str:
        return raw

    if expected_type is int:
        return int(raw)

    if expected_type is float:
        return float(raw)

    if expected_type is bool:
        return raw.lower() in ("1", "true", "yes", "y")

    if expected_type is date:
        # Accept YYYY-MM-DD
        return datetime.strptime(raw, "%Y-%m-%d").date()

    if expected_type is datetime:
        # Accept YYYY-MM-DD HH:MM:SS
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
        for fmt in formats:
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        raise ValueError(
            f"Cannot parse '{raw}' as datetime. Expected formats: {formats}"
        )

    # Fallback: try direct casting
    return expected_type(raw)
