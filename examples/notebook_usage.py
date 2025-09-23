"""
Simulate usage inside a Databricks notebook.

In real usage, dbutils is provided by Databricks.
Here, we can use a mock for local testing.
"""

from examples.sales_params import SalesParams
from tests.conftest import MockDbutils  # only for demo purposes


def main():
    # In Databricks → replace with real `dbutils`
    dbutils = MockDbutils()
    dbutils.widgets.text("market", "ES")

    # Initialize params
    params = SalesParams(dbutils)

    print("Market:", params.market)
    print("Environment:", params.env)
    print("Retries:", params.retries)


if __name__ == "__main__":
    main()
