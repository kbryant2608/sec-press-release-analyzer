# src/export.py

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

def assemble_records(
    mapping: Dict[str, str],
    filings: Dict[str, List[Dict]],
    extract_fn,
    clean_fn,
    sentiment_fn,
    keywords_fn,
    top_n_keywords: int = 5
) -> pd.DataFrame:
    """
    Build a DataFrame with one row per filing, containing:
      - ticker
      - cik
      - accessionNumber
      - filingDate
      - reportDate
      - raw_text
      - clean_text
      - sentiment (compound score)
      - top_keywords (as comma-separated string)
    """
    records: List[Dict[str, Any]] = []

    for ticker, cik in mapping.items():
        for f in filings.get(cik, []):
            accno = f["accessionNumber"]
            raw   = extract_fn(cik, accno)
            if not raw:
                continue
            clean  = clean_fn(raw)
            sent   = sentiment_fn(clean)["compound"]
            top_kw = keywords_fn([clean], top_n_keywords)
            keywords_str = ", ".join([kw for kw, _ in top_kw])

            records.append({
                "ticker":         ticker,
                "cik":            cik,
                "accessionNumber": accno,
                "filingDate":     f["filingDate"],
                "reportDate":     f["reportDate"],
                "raw_text":       raw,
                "clean_text":     clean,
                "sentiment":      sent,
                "top_keywords":   keywords_str
            })

    df = pd.DataFrame(records)
    return df

def export_to_csv(df: pd.DataFrame, path: str) -> None:
    """
    Save the DataFrame to CSV at `path`, creating parent folders if needed.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)
