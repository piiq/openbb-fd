"""Finance Database Provider module."""
from openbb_core.provider.abstract.provider import Provider

from openbb_fd.models.etf_search import FDEtfSearchFetcher
from openbb_fd.models.equity_search import FDEquitySearchFetcher
from openbb_fd.models.crypto_search import FDCryptoSearchFetcher

fd_provider = Provider(
    name="fd",
    website="https://github.com/JerBouma/FinanceDatabase",
    description="A community-managed database of 300.000+ tickers fully categorized.",
    fetcher_dict={
        "EtfSearch": FDEtfSearchFetcher,
        "EquitySearch": FDEquitySearchFetcher,
        "CryptoSearch": FDCryptoSearchFetcher,
    },
)
