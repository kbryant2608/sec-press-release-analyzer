# src/fetch_filings.py

import requests
from datetime import datetime
from typing import List, Dict

# SEC submissions URL template
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

def fetch_recent_8ks(
    ciks: List[str],
    count_per_cik: int = 5
) -> Dict[str, List[Dict]]:
    """
    For each CIK in `ciks`, fetch its submissions JSON from the SEC,
    filter for the most recent `count_per_cik` Form 8-K filings,
    and return a dict mapping CIK -> list of filings.

    Each filing dict includes at least:
      - 'accessionNumber'
      - 'reportDate'
      - 'filingDate'
      - 'form'
      - 'fileNumber'
    """
    results: Dict[str, List[Dict]] = {}

    for cik in ciks:
        url = SUBMISSIONS_URL.format(cik=cik)
        resp = requests.get(url, headers={"User-Agent": "Tesero tesero@yourdomain.com"})
        resp.raise_for_status()
        data = resp.json()

        # The filing history is under data['filings']['recent']
        recent = data.get("filings", {}).get("recent", {})
        forms     = recent.get("form", [])
        dates     = recent.get("filingDate", [])
        acc_nums  = recent.get("accessionNumber", [])
        report_ds = recent.get("reportDate", [])
        file_nums = recent.get("fileNumber", [])

        # Collect all 8-K entries in chronological order
        eight_ks = []
        for i, form in enumerate(forms):
            if form.upper() == "8-K":
                eight_ks.append({
                    "accessionNumber": acc_nums[i],
                    "filingDate":      dates[i],
                    "reportDate":      report_ds[i],
                    "form":            form,
                    "fileNumber":      file_nums[i],
                })

        # take the most recent `count_per_cik`
        # the SEC API returns filings newest first
        results[cik] = eight_ks[:count_per_cik]

    return results
