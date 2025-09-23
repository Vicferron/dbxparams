class DbxParamsError(Exception):
    """Base class for all dbxparams errors."""
    pass


class MissingParameterError(DbxParamsError):
    """Raised when a required parameter is not provided."""

    def __init__(self, name: str):
        message = (
            f"[MissingParameterError] Parameter '{name}' is required but was not provided.\n"
            f"Define it as a dbutils widget, add it to defaults, or set a class default."
        )
        super().__init__(message)


class InvalidTypeError(DbxParamsError):
    """Raised when a parameter value cannot be cast to the expected type."""

    def __init__(self, name: str, expected_type: type, value):
        message = (
            f"[InvalidTypeError] Parameter '{name}' expected type {expected_type.__name__} "
            f"but received value '{value}' (type {type(value).__name__}).\n"
            f"Ensure the widget/default matches the declared type."
        )
        super().__init__(message)


class ValidationError(DbxParamsError):
    """Raised when a custom validation fails."""

    def __init__(self, name: str, reason: str):
        message = (
            f"[ValidationError] Parameter '{name}' failed validation.\n"
            f"Reason: {reason}"
        )
        super().__init__(message)
