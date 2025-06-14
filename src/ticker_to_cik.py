# src/ticker_to_cik.py

import requests

# Constants for SEC EDGAR
SEC_HEADERS = {
    "User-Agent": "Tesero tesero@yourdomain.com",
    "Accept": "application/json"
}
TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"

def get_cik_mapping() -> dict[str, str]:
    """
    Fetch the SEC master ticker → CIK mapping,
    returning a dict where keys are uppercase tickers
    and values are zero-padded 10-digit CIK strings.
    """
    resp = requests.get(TICKER_CIK_URL, headers=SEC_HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return {
        item["ticker"].upper(): str(item["cik_str"]).zfill(10)
        for item in data.values()
    }

def lookup_cik(tickers: list[str]) -> dict[str, str | None]:
    """
    Given a list of ticker symbols, return a dict mapping
    each ticker (uppercase) to its CIK (or None if not found).
    """
    mapping = get_cik_mapping()
    return {t.upper(): mapping.get(t.upper()) for t in tickers}
