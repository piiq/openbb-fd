# Finance Database provider for OpenBB

Finance Database by Jeroen Bouma offers an extensive collection of over 300,000 symbols across various financial instruments, including Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies, and Money Markets. It's designed to provide a comprehensive overview of sectors, industries, and types of investments.

## Introduction

This extension integrates the Finance Database datasets into OpenBB. It enhances the capabilities of OpenBB’s equity, crypto, and ETF search functionalities. This integration adds capabilities to search through a broad spectrum of financial instruments.

## Installation

To install this extension, you can use pip:

```bash
pip install openbb-fd
```

Alternatively, for the latest version directly from the repository:

```bash
pip install git+https://github.com/piiq/openbb-fd.git
```

## Usage

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
