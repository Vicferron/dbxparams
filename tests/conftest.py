import pytest


class MockWidgets:
    """Simulate dbutils.widgets behavior for testing."""

    def __init__(self):
        self._store = {}

    def text(self, name: str, defaultValue: str = "", label: str = ""):
        """Simulate creating a text widget (store default)."""
        self._store[name] = str(defaultValue)

    def get(self, name: str) -> str:
        """Return stored widget value."""
        if name not in self._store:
            raise Exception(f"Widget '{name}' not found")
        return self._store[name]

    def set(self, name: str, value: str):
        """Update an existing widget value."""
        if name not in self._store:
            raise Exception(f"Widget '{name}' not found")
        self._store[name] = str(value)


class MockDbutils:
    """Simulate dbutils object with widgets API."""

    def __init__(self):
        self.widgets = MockWidgets()


@pytest.fixture
def mock_dbutils():
    """Fixture that provides a fresh MockDbutils for each test."""
    return MockDbutils()
