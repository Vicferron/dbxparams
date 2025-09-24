from typing import Any, Dict, get_type_hints
from .errors import MissingParameterError, InvalidTypeError
from .types import cast_value


class NotebookParams:
    def __init__(self, dbutils: Any = None, defaults: Dict[str, Any] = None):
        """
        Initialize parameters.

        Args:
            dbutils: Databricks dbutils instance (optional in debug mode).
            defaults: Dict with fallback values for local/debug runs.
        """
        self._dbutils = dbutils
        self._defaults = defaults or {}
        self._parse_class_annotations()

    def _parse_class_annotations(self):
        """Read type annotations from subclass and assign values."""
        type_hints = get_type_hints(self.__class__)

        for name, type_hint in type_hints.items():
            default = getattr(self, name, None)
            if self._dbutils:
                try:
                    # Create widget if it does not exist
                    self._dbutils.widgets.text(
                        name, str(default) if default is not None else ""
                    )
                except Exception:
                    # Ignore if widget already exists
                    pass
            value = self._get_value(name, type_hint, default)
            setattr(self, name, value)

    def _get_value(self, name: str, type_hint: Any, default: Any):
        """
        Resolve parameter value:
        - From dbutils.widgets if available
        - Else from defaults dict
        - Else from class default
        - Else raise MissingParameterError
        """
        val = None

        # 1. Try dbutils.widgets
        if self._dbutils:
            try:
                val = self._dbutils.widgets.get(name)
            except Exception:
                pass

        # 2. Fallback to defaults dict
        if val is None and name in self._defaults:
            val = self._defaults[name]

        # 3. Fallback to class default
        if val is None and default is not None:
            val = default

        # 4. Error if still None or empty string
        if val is None or (isinstance(val, str) and val.strip() == ""):
            raise MissingParameterError(name)

        # 5. Validate type if hint provided
        try:
            return cast_value(val, type_hint) if type_hint else val
        except Exception:
            raise InvalidTypeError(name, type_hint, val)
