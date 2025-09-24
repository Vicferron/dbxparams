import pytest
from dbxparams import NotebookParams, MissingParameterError, InvalidTypeError
from datetime import date, datetime


# ---------- Example classes ----------
class BasicParams(NotebookParams):
    market: str  # required
    env: str = "dev"  # optional with default
    retries: int = 3  # optional with default


class TypedParams(NotebookParams):
    threshold: float
    active: bool


class DateParams(NotebookParams):
    start_date: date
    end_time: datetime


class IntParams(NotebookParams):
    retries: int


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
    assert params.env == "dev"
    assert params.retries == 3


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
    """Should raise InvalidTypeError if type conversion fails (float)."""
    mock_dbutils.widgets.text("threshold", "not-a-float")
    mock_dbutils.widgets.text("active", "true")

    with pytest.raises(InvalidTypeError):
        TypedParams(mock_dbutils)


def test_date_and_datetime_success(mock_dbutils):
    """Should correctly parse date and datetime strings."""
    mock_dbutils.widgets.text("start_date", "2025-10-01")
    mock_dbutils.widgets.text("end_time", "2025-10-01 12:30:00")

    params = DateParams(mock_dbutils)

    assert isinstance(params.start_date, date)
    assert params.start_date == date(2025, 10, 1)

    assert isinstance(params.end_time, datetime)
    assert params.end_time == datetime(2025, 10, 1, 12, 30, 0)


def test_date_failure(mock_dbutils):
    """Should raise InvalidTypeError if date format is invalid."""
    mock_dbutils.widgets.text("start_date", "01-10-2025")
    mock_dbutils.widgets.text("end_time", "2025-10-01 12:30:00")

    with pytest.raises(InvalidTypeError):
        DateParams(mock_dbutils)


def test_datetime_failure(mock_dbutils):
    """Should raise InvalidTypeError if datetime format is invalid."""
    mock_dbutils.widgets.text("start_date", "2025-10-01")
    mock_dbutils.widgets.text("end_time", "invalid-datetime")

    with pytest.raises(InvalidTypeError):
        DateParams(mock_dbutils)


def test_bool_invalid_value(mock_dbutils):
    """Should raise InvalidTypeError if bool value is not supported."""
    mock_dbutils.widgets.text("threshold", "3.14")
    mock_dbutils.widgets.text("active", "maybe")

    with pytest.raises(InvalidTypeError):
        TypedParams(mock_dbutils)


def test_int_success(mock_dbutils):
    """Should cast int correctly."""
    mock_dbutils.widgets.text("retries", "5")
    params = IntParams(mock_dbutils)
    assert isinstance(params.retries, int)
    assert params.retries == 5


def test_int_failure(mock_dbutils):
    """Should raise InvalidTypeError if int format is invalid."""
    mock_dbutils.widgets.text("retries", "five")
    with pytest.raises(InvalidTypeError):
        IntParams(mock_dbutils)


def test_empty_string_is_missing(mock_dbutils):
    """Empty string should be treated as missing -> MissingParameterError."""
    mock_dbutils.widgets.text("market", "")
    with pytest.raises(MissingParameterError):
        BasicParams(mock_dbutils)
