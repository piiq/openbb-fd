from openbb_fd.models.etf_search import FDEtfSearchFetcher
from openbb_fd.models.equity_search import FDEquitySearchFetcher
from openbb_fd.models.crypto_search import FDCryptoSearchFetcher


# NOTE: I'm not using @pytest.mark.record_http because I don't want to
#       keep 7 megabyte base64 encoded csvs in as mock data.
def test_fd_etf_search_fetcher():
    params = {
        "query": "IOO",
    }

    fetcher = FDEtfSearchFetcher()
    result = fetcher.test(params)
    assert result is None


def test_fd_equity_search_fetcher():
    params = {
        "query": "ZILL",
    }

    fetcher = FDEquitySearchFetcher()
    result = fetcher.test(params)
    assert result is None


def test_fd_crypto_search_fetcher():
    params = {
        "query": "ZILL",
    }

    fetcher = FDCryptoSearchFetcher()
    result = fetcher.test(params)
    assert result is None
