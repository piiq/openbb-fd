# Finance Database provider for OpenBB

Finance Database by Jeroen Bouma offers an extensive collection of over 300,000 symbols across various financial instruments, including Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies, and Money Markets. It's designed to provide a comprehensive overview of sectors, industries, and types of investments.

## Introduction

This extension integrates the Finance Database datasets into OpenBB. It enhances the capabilities of OpenBB’s equity, crypto, and ETF search functionalities. This integration adds capabilities to search through a broad spectrum of financial instruments.

## Requirements

- Python 3.12+
- OpenBB Core 2.0.1+
- `uv` for local development

## Installation

Add the provider and the asset routers used by the examples to your uv project:

```bash
uv add openbb-fd openbb-equity openbb-etf openbb-crypto
```

Alternatively, for the latest version directly from the repository:

```bash
uv add git+https://github.com/piiq/openbb-fd.git
```

Rebuild the generated interface after changing installed extensions:

```bash
uv run openbb-build
```

## Local development

```bash
uv sync --locked
uv run openbb-build
uv run pytest
uv run ruff check .
uv run ty check
uv run rumdl check --config pyproject.toml README.md
```

The development group installs the equity, ETF, and crypto routers for the generated `obb` interface, plus the Platform API for HTTP integration tests. OpenBB 5 installs these asset routers through its optional `routers` extra; a provider installation alone does not install them.

Run the API and the live integration tests in separate terminals:

```bash
uv run openbb-api --host 127.0.0.1 --port 8000
uv run pytest integration
```

## Usage

```python
from openbb import obb
```

Here are some command examples to demonstrate the usage of this integration:

To search for equities in a defense industry:

```bash
>>> sample = obb.equity.search(query="Defense", provider="fd")
>>> print(f"Total companies in the sample: {len(sample.to_df()['name'].unique())}")
Total companies in the sample: 880
```

To find ETFs matching certain criteria:

```python
>>> sample = obb.etf.search(query="Wheat", provider="fd")
>>> print(f"Total etfs in the sample: {len(sample.to_df()['name'].unique())}")
Total etfs in the sample: 10
```

For cryptocurrency analysis:

```python
>>> sample = obb.crypto.search(query="node", provider="fd")
>>> print(f"Total cryptos in the sample: {len(sample.to_df()['name'].unique())}")
Total cryptos in the sample: 10
```

## License

This project is licensed under the MIT License.
