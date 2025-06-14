# src/parse_exhibits.py

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

SEC_BASE = "https://www.sec.gov/Archives"
USER_AGENT = {"User-Agent": "Tesero tesero@yourdomain.com"}

def extract_exhibit_99_1(cik: str, accession_number: str) -> Optional[str]:
    """
    Given a zero-padded CIK and an accession number (with dashes),
    find the Exhibit 99.1 HTML file, fetch it, and return its text.
    Returns None if no matching exhibit is found.
    """
    # Build the path components
    no_dash = accession_number.replace("-", "")
    index_json_url = f"{SEC_BASE}/edgar/data/{int(cik)}/{no_dash}/index.json"

    resp = requests.get(index_json_url, headers=USER_AGENT)
    resp.raise_for_status()
    files = resp.json().get("directory", {}).get("item", [])

    # Look for any “ex…” exhibit or R1.htm (common press-release container)
    pattern = re.compile(r"(?:ex\d[-_.]\d|r1)\.htm$", re.IGNORECASE)

    target = next((f["name"] for f in files if pattern.search(f["name"])), None)
    if not target:
        return None

    # Fetch and parse the exhibit HTML
    exhibit_url = f"{SEC_BASE}/edgar/data/{int(cik)}/{no_dash}/{target}"
    exhibit_resp = requests.get(exhibit_url, headers=USER_AGENT)
    exhibit_resp.raise_for_status()

    soup = BeautifulSoup(exhibit_resp.text, "lxml")
    # Grab the main body text
    texts = soup.get_text(separator="\n")
    # Clean up excessive whitespace
    return "\n".join(line.strip() for line in texts.splitlines() if line.strip())
