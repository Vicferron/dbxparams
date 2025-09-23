import pytest
from dbxparams import NotebookParams, MissingParameterError, InvalidTypeError


# ---------- Example classes for tests ----------
class BasicParams(NotebookParams):
    market: str  # required
    env: str = "dev"  # optional with default
    retries: int = 3  # optional with default


class TypedParams(NotebookParams):
    threshold: float
    active: bool


# ---------- Tests ----------

def test_required_param_missing(mock_dbutils):
    """Should raise error if required param is not provided anywhere."""
    with pytest.raises(MissingParameterError):
        BasicParams(mock_dbutils)


def test_required_param_from_widget(mock_dbutils):
    """Should read required param from dbutils.widgets."""
    mock_dbutils.widgets.text("market", "ES")

    params = BasicParams(mock_dbutils)

    assert params.market == "ES"
    assert params.env == "dev"  # default from class
    assert params.retries == 3  # default from class


def test_required_param_from_defaults_dict():
    """Should read required param from defaults dict when no widget exists."""
    params = BasicParams(None, defaults={"market": "FR"})

    assert params.market == "FR"
    assert params.env == "dev"
    assert params.retries == 3


def test_type_casting_success(mock_dbutils):
    """Should cast types correctly (float, bool)."""
    mock_dbutils.widgets.text("threshold", "3.14")
    mock_dbutils.widgets.text("active", "true")

    params = TypedParams(mock_dbutils)

    assert isinstance(params.threshold, float)
    assert params.threshold == 3.14
    assert isinstance(params.active, bool)
    assert params.active is True


def test_type_casting_failure(mock_dbutils):
    """Should raise InvalidTypeError if type conversion fails."""
    mock_dbutils.widgets.text("threshold", "not-a-float")
    mock_dbutils.widgets.text("active", "true")

    with pytest.raises(InvalidTypeError):
        TypedParams(mock_dbutils)
