"""FD Equity Search."""

from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.equity_search import (
    EquitySearchData,
    EquitySearchQueryParams,
)
from pydantic import Field
from ..utils.helpers import get_dataset


class FDEquitySearchQueryParams(EquitySearchQueryParams):
    """FD Equity Search Query Params."""


class FDEquitySearchData(EquitySearchData):
    """FD Equity Search Data."""

    description: Optional[str] = Field(
        description="A description of the company.",
        alias="summary",
        default=None,
    )

    currency: Optional[str] = Field(
        description="The currency the equity is traded in.",
    )

    sector: Optional[str] = Field(
        description="The sector the company belongs to.",
        default=None,
    )

    industry_group: Optional[str] = Field(
        description="The industry group the company belongs to.",
        default=None,
    )

    industry: Optional[str] = Field(
        description="The industry the company belongs to.",
        default=None,
    )

    exchange: Optional[str] = Field(
        description="The exchange code the equity trades on.",
        default=None,
    )

    market: Optional[str] = Field(
        description="The market the equity trades on.",
        default=None,
    )

    country: Optional[str] = Field(
        description="The country of the company's address.",
        default=None,
    )

    state: Optional[str] = Field(
        description="The state of the company's address.",
        default=None,
    )

    city: Optional[str] = Field(
        description="The city of the company's address.",
        default=None,
    )

    zipcode: Optional[str] = Field(
        description="The zipcode of the company's address.",
        default=None,
    )

    website: Optional[str] = Field(
        description="The website of the company.",
        default=None,
    )

    market_cap: Optional[str] = Field(
        description="The market cap of the company.",
        default=None,
    )

    isin: Optional[str] = Field(
        description="The ISIN of the equity.",
        default=None,
    )

    cusip: Optional[str] = Field(
        description="The CUSIP of the equity.",
        default=None,
    )

    figi: Optional[str] = Field(
        description="The FIGI of the equity.",
        default=None,
    )

    composite_figi: Optional[str] = Field(
        description="The composite FIGI of the equity.",
        default=None,
    )

    shareclass_figi: Optional[str] = Field(
        description="The shareclass FIGI of the equity.",
        default=None,
    )


class FDEquitySearchFetcher(
    Fetcher[
        FDEquitySearchQueryParams,
        List[FDEquitySearchData],
    ]
):
    """Transform the query, extract and transform the data from the FD endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> FDEquitySearchQueryParams:
        """Transform the query."""
        return FDEquitySearchQueryParams(**params)

    @staticmethod
    def extract_data(  # pylint: disable=unused-argument
        query: FDEquitySearchQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the FD endpoint."""
        equities = get_dataset("equities")

        if query.query:
            equities = equities[
                equities["symbol"].str.contains(query.query, case=False)
                | equities["name"].str.contains(query.query, case=False)
                | equities["summary"].str.contains(query.query, case=False)
                | equities["currency"].str.contains(query.query, case=False)
                | equities["sector"].str.contains(query.query, case=False)
                | equities["industry_group"].str.contains(query.query, case=False)
                | equities["industry"].str.contains(query.query, case=False)
                | equities["exchange"].str.contains(query.query, case=False)
                | equities["market"].str.contains(query.query, case=False)
                | equities["country"].str.contains(query.query, case=False)
                | equities["state"].str.contains(query.query, case=False)
                | equities["city"].str.contains(query.query, case=False)
                | equities["zipcode"].str.contains(query.query, case=False)
                | equities["website"].str.contains(query.query, case=False)
                | equities["market_cap"].str.contains(query.query, case=False)
                | equities["isin"].str.contains(query.query, case=False)
                | equities["cusip"].str.contains(query.query, case=False)
                | equities["figi"].str.contains(query.query, case=False)
                | equities["composite_figi"].str.contains(query.query, case=False)
                | equities["shareclass_figi"].str.contains(query.query, case=False)
            ]
        for col in equities:
            if equities[col].dtype in ("int", "float"):
                equities[col] = equities[col].fillna(0)
            elif equities[col].dtype == "string":
                equities[col] = equities[col].fillna("")
        return equities.to_dict("records")

    @staticmethod
    def transform_data(  # pylint: disable=unused-argument
        query: FDEquitySearchQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[FDEquitySearchData]:
        """Return the transformed data."""
        return [FDEquitySearchData.model_validate(d) for d in data]
