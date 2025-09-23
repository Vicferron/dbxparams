# dbxparams

A lightweight library to manage **Databricks notebook parameters** as Python classes.
Stop repeating `dbutils.widgets` code in every notebook — define your parameters once as a class, and let dbxparams handle the rest.

---

## 🚀 Features

* Define parameters as **Python classes** with type annotations.
* Automatically **create and read widgets** from `dbutils`.
* Support for **required and optional parameters** (with defaults).
* Simple **type validation** (`str`, `int`, `float`, `bool`, `date`, `datetime`).
* Clear and **verbose error messages**.
* **Debug mode** with fallback `defaults` dictionary for local runs.

---

## 📦 Installation

```
pip install dbxparams
```

---

## 📝 Usage

### 1. Define your parameter class

```python
from dbxparams import NotebookParams

class SalesParams(NotebookParams):
    market: str             # required
    env: str = "dev"        # optional with default
    retries: int = 3        # optional with default
```

### 2. Use it inside your notebook

```python
params = SalesParams(dbutils)

print(params.market)   # value from widget or defaults
print(params.env)      # "dev" (default)
print(params.retries)  # 3 (default)
```

### 3. Debug locally (without Databricks)

```python
params = SalesParams(None, defaults={"market": "FR"})
print(params.market)  # "FR"
```

---

## ⚠️ Errors & Validations

* **MissingParameterError**
  Raised if a required parameter is not defined anywhere.

* **InvalidTypeError**
  Raised if the value cannot be cast to the expected type.

* **ValidationError**
  Reserved for custom validations (e.g., regex, ranges).

Example:

```
[InvalidTypeError] Parameter 'threshold' expected type float
but received value 'abc' (type str).
💡 Ensure the widget/default matches the declared type.
```

---

## 📚 Roadmap

* Load parameters from **JSON/YAML configs**.
* Extended type support (lists, enums, regex validations).
* Better integration with Databricks Jobs parameters.

---

## 🤝 Contributing

Contributions are welcome!
Open an issue or submit a pull request on GitHub.

---

## 📄 License

MIT License. See LICENSE for details.

Copyright (c) 2025 Víctor Ferrón Álvarez
https://vicferron.github.io/
