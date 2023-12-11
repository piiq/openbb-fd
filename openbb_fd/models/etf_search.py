"""FD ETF Search."""

from typing import Any, Dict, List, Optional

# import pandas as pd
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.etf_search import (
    EtfSearchData,
    EtfSearchQueryParams,
)
from pydantic import Field
from ..utils.helpers import get_dataset


class FDEtfSearchQueryParams(EtfSearchQueryParams):
    """FD ETF Search Query Params."""


class FDEtfSearchData(EtfSearchData):
    """FD ETF Search Data."""

    currency: Optional[str] = Field(
        description="The currency the ETF is traded in.",
    )
    description: Optional[str] = Field(
        description="A description of the ETF.",
        alias="summary",
        default=None,
    )
    category_group: Optional[str] = Field(
        description="The category group the ETF belongs to.",
        default=None,
    )
    category: Optional[str] = Field(
        description="The category the ETF belongs to.",
        default=None,
    )
    family: Optional[str] = Field(
        description="The family the ETF belongs to.",
        default=None,
    )
    exchange: Optional[str] = Field(
        description="The exchange code the ETF trades on.",
        default=None,
    )
    market: Optional[str] = Field(
        description="The market the ETF trades on.",
        default=None,
    )


class FDEtfSearchFetcher(
    Fetcher[
        FDEtfSearchQueryParams,
        List[FDEtfSearchData],
    ]
):
    """Transform the query, extract and transform the data from the FD endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> FDEtfSearchQueryParams:
        """Transform the query."""
        return FDEtfSearchQueryParams(**params)

    @staticmethod
    def extract_data(  # pylint: disable=unused-argument
        query: FDEtfSearchQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the FD endpoint."""
        etfs = get_dataset("etfs")

        if query.query:
            etfs = etfs[
                etfs["symbol"].str.contains(query.query, case=False)
                | etfs["name"].str.contains(query.query, case=False)
                | etfs["currency"].str.contains(query.query, case=False)
                | etfs["summary"].str.contains(query.query, case=False)
                | etfs["category_group"].str.contains(query.query, case=False)
                | etfs["category"].str.contains(query.query, case=False)
                | etfs["family"].str.contains(query.query, case=False)
                | etfs["exchange"].str.contains(query.query, case=False)
                | etfs["market"].str.contains(query.query, case=False)
            ]
        for col in etfs:
            if etfs[col].dtype in ("int", "float"):
                etfs[col] = etfs[col].fillna(0)
            elif etfs[col].dtype == "string":
                etfs[col] = etfs[col].fillna("")
        return etfs.to_dict("records")

    @staticmethod
    def transform_data(  # pylint: disable=unused-argument
        query: FDEtfSearchQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[FDEtfSearchData]:
        """Return the transformed data."""
        return [FDEtfSearchData.model_validate(d) for d in data]
