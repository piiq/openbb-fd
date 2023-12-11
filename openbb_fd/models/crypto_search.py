"""FD Crypto Search."""

from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.crypto_search import (
    CryptoSearchData,
    CryptoSearchQueryParams,
)
from pydantic import Field
from ..utils.helpers import get_dataset


class FDCryptoSearchQueryParams(CryptoSearchQueryParams):
    """FD Crypto Search Query Params."""


class FDCryptoSearchData(CryptoSearchData):
    """FD Crypto Search Data."""

    __alias_dict__ = {"symbol": "cryptocurrency"}

    exchange_symbol: Optional[str] = Field(
        description="The exchange symbol of the cryptocurrency.",
        alias="symbol",
        default=None,
    )
    currency: Optional[str] = Field(
        description="The currency the crypto is traded in.",
    )
    description: Optional[str] = Field(
        description="A description of the crypto.",
        alias="summary",
        default=None,
    )
    exchange: Optional[str] = Field(
        description="The exchange code the crypto trades on.",
        default=None,
    )
    market: Optional[str] = Field(
        description="The market the crypto trades on.",
        default=None,
    )


class FDCryptoSearchFetcher(
    Fetcher[
        FDCryptoSearchQueryParams,
        List[FDCryptoSearchData],
    ]
):
    """Transform the query, extract and transform the data from the FD endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> FDCryptoSearchQueryParams:
        """Transform the query."""
        return FDCryptoSearchQueryParams(**params)

    @staticmethod
    def extract_data(  # pylint: disable=unused-argument
        query: FDCryptoSearchQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the FD endpoint."""
        cryptos = get_dataset("cryptos")

        if query.query:
            cryptos = cryptos[
                cryptos["symbol"].str.contains(query.query, case=False)
                | cryptos["cryptocurrency"].str.contains(query.query, case=False)
                | cryptos["name"].str.contains(query.query, case=False)
                | cryptos["currency"].str.contains(query.query, case=False)
                | cryptos["summary"].str.contains(query.query, case=False)
                | cryptos["exchange"].str.contains(query.query, case=False)
                | cryptos["market"].str.contains(query.query, case=False)
            ]
        for col in cryptos:
            if cryptos[col].dtype in ("int", "float"):
                cryptos[col] = cryptos[col].fillna(0)
            elif cryptos[col].dtype == "string":
                cryptos[col] = cryptos[col].fillna("")
        return cryptos.to_dict("records")

    @staticmethod
    def transform_data(  # pylint: disable=unused-argument
        query: FDCryptoSearchQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[FDCryptoSearchData]:
        """Return the transformed data."""
        return [FDCryptoSearchData.model_validate(d) for d in data]
