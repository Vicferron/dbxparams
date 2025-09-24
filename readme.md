# dbxparams

[![PyPI version](https://badge.fury.io/py/dbxparams.svg)](https://pypi.org/project/dbxparams/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dbxparams.svg)](https://pypi.org/project/dbxparams/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight library for managing **Databricks notebook parameters** with type safety, defaults, and automatic widget creation.

---

## ✨ Features

- Auto-create and populate **Databricks widgets**
- Type-safe parameter casting (`int`, `float`, `bool`, `date`, `datetime`)
- Support for **defaults dict** and class defaults
- Custom error handling: `MissingParameterError`, `InvalidTypeError`
- Cleaner, more maintainable notebooks (no more repetitive `dbutils.widgets.get`!)

---

## 📦 Installation

```bash
pip install dbxparams
```

---

## 🚀 Quick Start

```python
from dbxparams import NotebookParams

class MyParams(NotebookParams):
    market: str              # required
    env: str = "dev"         # optional with default
    retries: int = 3         # optional with default

# Pass dbutils to auto-create widgets and populate values
params = MyParams(dbutils)

print(params.market)   # Read from widget
print(params.env)      # Uses default "dev" if not set
print(params.retries)  # Uses default 3
```

---

## 🔒 Error Handling

- **MissingParameterError** → Raised when a required parameter is missing
- **InvalidTypeError** → Raised when a value cannot be cast to the expected type

Example:
```python
class TypedParams(NotebookParams):
    threshold: float
    active: bool

# If "threshold" widget is "not-a-float" → InvalidTypeError
```

---


## 📜 License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2025 Víctor Ferrón Álvarez
https://vicferron.github.io/
