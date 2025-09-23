from dbxparams import NotebookParams


class SalesParams(NotebookParams):
    """
    Example parameter class for a sales ETL pipeline.
    """

    market: str  # required
    env: str = "dev"  # optional with default
    retries: int = 3  # optional with default
