import pytest

class MockWidgets:
    """Simulate dbutils.widgets behavior for testing."""

    def __init__(self):
        self._store = {}

    def text(self, name: str, defaultValue: str = "", label: str = ""):
        """Create a text widget. If it already exists, raise (like Databricks)."""
        if name in self._store:
            raise Exception(f"Widget '{name}' already exists")
        self._store[name] = str(defaultValue)

    def get(self, name: str) -> str:
        if name not in self._store:
            raise Exception(f"Widget '{name}' not found")
        return self._store[name]

    def set(self, name: str, value: str):
        if name not in self._store:
            raise Exception(f"Widget '{name}' not found")
        self._store[name] = str(value)


class MockDbutils:
    def __init__(self):
        self.widgets = MockWidgets()


@pytest.fixture
def mock_dbutils():
    return MockDbutils()
