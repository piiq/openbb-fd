"""Helper for downloading data to a local location."""
import os
from typing import Literal

import pandas as pd
import requests

GITHUB_ROOT_URL = "https://raw.githubusercontent.com/"
GITHUB_DATA_FOLDER = "JerBouma/FinanceDatabase/main/compression/"
LOCAL_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")

_dataset = Literal[
    "cryptos", "currencies", "equities", "etfs", "funds", "indices", "moneymarkets"
]


def _get_github_etag(dataset: _dataset) -> str:
    """Get ETag for a dataset on GitHub."""
    url = GITHUB_ROOT_URL + GITHUB_DATA_FOLDER + f"{dataset}.bz2"
    response = requests.head(url, timeout=1)
    return response.headers.get("ETag", "")


def _get_saved_etag(dataset: _dataset) -> str:
    """Get saved ETag for a dataset."""
    etag_file = os.path.join(LOCAL_FOLDER, f"{dataset}.etag")
    if os.path.exists(etag_file):
        with open(etag_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def _save_etag(dataset: _dataset, etag: str) -> None:
    """Save ETag for a dataset."""
    etag_file = os.path.join(LOCAL_FOLDER, f"{dataset}.etag")
    with open(etag_file, "w", encoding="utf-8") as f:
        f.write(etag)


def _download_and_save(dataset: _dataset) -> None:
    """Download and save dataset from GitHub."""
    if not os.path.exists(LOCAL_FOLDER):
        os.makedirs(LOCAL_FOLDER)
    print(f"Downloading {dataset}...")
    url = GITHUB_ROOT_URL + GITHUB_DATA_FOLDER + f"{dataset}.bz2"
    data = pd.read_csv(url, compression="bz2", header=0)
    data.to_csv(os.path.join(LOCAL_FOLDER, f"{dataset}.csv"), index=False)
    etag = _get_github_etag(dataset)
    if etag:
        _save_etag(dataset, etag)


def get_dataset(dataset: _dataset) -> pd.DataFrame:
    """Get dataset from the data directory."""
    local_path = os.path.join(LOCAL_FOLDER, f"{dataset}.csv")
    if not os.path.exists(local_path):
        _download_and_save(dataset)
    else:
        saved_etag = _get_saved_etag(dataset)
        current_etag = _get_github_etag(dataset)
        if saved_etag != current_etag:
            _download_and_save(dataset)
    return pd.read_csv(local_path, header=0).convert_dtypes()
