"""Offline tests for Finance Database search through OpenBB's interfaces."""

import importlib

import pandas as pd
import pytest

from openbb_fd.models.crypto_search import FDCryptoSearchFetcher
from openbb_fd.models.equity_search import FDEquitySearchFetcher
from openbb_fd.models.etf_search import FDEtfSearchFetcher
from openbb_fd.utils import helpers

FETCHERS = {
    "equity": FDEquitySearchFetcher,
    "etf": FDEtfSearchFetcher,
    "crypto": FDCryptoSearchFetcher,
}


@pytest.fixture(params=FETCHERS)
def search(request, monkeypatch):
    """Supply nullable string columns matching each Finance Database dataset."""
    asset = request.param
    module = importlib.import_module(f"openbb_fd.models.{asset}_search")
    fetcher = FETCHERS[asset]
    columns = {
        "equity": [
            "symbol", "name", "summary", "currency", "sector", "industry_group", "industry", "exchange",
            "market", "country", "state", "city", "zipcode", "website", "market_cap", "isin", "cusip",
            "figi", "composite_figi", "shareclass_figi",
        ],
        "etf": ["symbol", "name", "currency", "summary", "category_group", "category", "family", "exchange", "market"],
        "crypto": ["symbol", "cryptocurrency", "name", "currency", "summary", "exchange", "market"],
    }[asset]
    rows = [dict.fromkeys(columns) for _ in range(2)]
    rows[0].update(symbol="001", name="Alpha", summary="First asset", currency="USD")
    rows[1].update(symbol="002", name="Beta")
    if asset == "crypto":
        rows[0]["cryptocurrency"] = "ALPHA"
        rows[1]["cryptocurrency"] = "BETA"
    if asset == "equity":
        rows[0]["zipcode"] = "00123"
    frame = pd.DataFrame(rows, dtype="string")
    monkeypatch.setattr(module, "get_dataset", lambda _: frame)
    return asset, fetcher


def test_fetcher_contract_handles_missing_values(search):
    """All rows should validate with the current OpenBB Fetcher and pandas."""
    _, fetcher = search
    fetcher.test({"query": ""})
    query = fetcher.transform_query({"query": ""})
    result = fetcher.transform_data(query, fetcher.extract_data(query, credentials=None))
    assert len(result) == 2
    assert result[0].description == "First asset"
    assert result[1].description is None
    assert result[1].currency is None


def test_search_filters_nullable_columns(search):
    """Search should retain matches when other searchable fields are missing."""
    _, fetcher = search
    query = fetcher.transform_query({"query": "alpha"})
    result = fetcher.transform_data(query, fetcher.extract_data(query, credentials=None))
    assert len(result) == 1
    assert result[0].name == "Alpha"


def test_equity_symbol_search(monkeypatch):
    """The standard is_symbol parameter should restrict matching to symbols."""
    module = importlib.import_module("openbb_fd.models.equity_search")
    frame = pd.DataFrame({"symbol": ["ABC", "XYZ"], "name": ["XYZ Holdings", "ABC Holdings"]}, dtype="string")
    monkeypatch.setattr(module, "get_dataset", lambda _: frame)
    query = FDEquitySearchFetcher.transform_query({"query": "abc", "is_symbol": True})
    assert FDEquitySearchFetcher.extract_data(query, credentials=None) == [{"symbol": "ABC", "name": "XYZ Holdings"}]


def test_dataset_preserves_numeric_identifiers_and_nulls(tmp_path, monkeypatch):
    """CSV inference must preserve zero-prefixed symbols and ZIP codes."""
    (tmp_path / "equities.csv").write_text("symbol,name,currency,zipcode\n001,Alpha,USD,00123\n002,Beta,,\n")
    monkeypatch.setattr(helpers, "LOCAL_FOLDER", str(tmp_path))
    monkeypatch.setattr(helpers, "_get_github_etag", lambda _: "")
    frame = helpers.get_dataset("equities")
    assert frame.loc[0, "symbol"] == "001"
    assert frame.loc[0, "zipcode"] == "00123"
    assert pd.isna(frame.loc[1, "currency"])


def test_generated_python_search(search):
    """The provider entry point must execute through the generated obb API."""
    from openbb import obb

    asset, _ = search
    result = getattr(obb, asset).search(query="alpha", provider="fd")
    assert result.provider == "fd"
    assert len(result.results) == 1
    assert result.results[0].name == "Alpha"
    assert len(result.to_df()) == 1
    if asset == "crypto":
        assert result.results[0].symbol == "ALPHA"
        assert result.results[0].exchange_symbol == "001"


def test_http_search(search):
    """The same provider should execute through OpenBB's generated HTTP route."""
    from fastapi.testclient import TestClient
    from openbb_core.api.rest_api import app

    asset, _ = search
    response = TestClient(app).get(f"/api/v1/{asset}/search", params={"query": "alpha", "provider": "fd"})
    assert response.status_code == 200, response.text
    assert response.json()["results"][0]["name"] == "Alpha"
