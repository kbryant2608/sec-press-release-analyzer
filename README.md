# SEC EDGAR Press Release Analyzer

A **Python**–based pipeline and **Jupyter Notebook** for automating the retrieval, extraction, and analysis of Form 8‑K press releases (Exhibit 99.1) from the SEC’s EDGAR system.

## 🔍 Features

* **Ticker→CIK Mapping:** Converts stock symbols into SEC Central Index Keys.
* **8‑K Filings Fetcher:** Downloads recent Form 8‑K metadata via EDGAR’s submissions API.
* **Exhibit Extraction:** Identifies and pulls the correct Exhibit 99.1 HTML (or equivalent) for each filing.
* **Text Cleaning & NLP:** Lowercases, strips boilerplate, then runs sentiment (VADER) and keyword (TF‑IDF) analyses.
* **Data Export:** Compiles results into a `press_releases_summary.csv` for downstream reporting or visualization.

## 🚀 Quick Start

1. **Clone** the repo and navigate into it:

   ```bash
   git clone https://github.com/kbryant2608/sec-press-release-analyzer.git
   cd sec-press-release-analyzer
   ```
2. **Create a virtual environment** and **activate** it:

   ```bash
   python3 -m venv venv      # macOS/Linux
   source venv/bin/activate  # macOS/Linux

   python -m venv venv       # Windows PowerShell
   .\\venv\\Scripts\\Activate.ps1  # Windows
   ```
3. **Install** dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Launch** JupyterLab and open the notebook:

   ```bash
   pip install jupyterlab ipykernel
   python -m ipykernel install --user --name=sec-analyzer-venv --display-name "Python (sec-analyzer)"
   jupyter lab
   ```
5. **Run** each step in `notebooks/sec_press_release_analyzer.ipynb` (Step 1 through Step 6).
6. **Find** `press_releases_summary.csv` in the `outputs/` folder.

## 📦 Project Structure

```
sec-press-release-analyzer/
├── notebooks/                # Jupyter notebook orchestration
│   └── sec_press_release_analyzer.ipynb
├── src/                      # Modular Python code for each pipeline stage
│   ├── ticker_to_cik.py
│   ├── fetch_filings.py
│   ├── parse_exhibits.py
│   ├── text_analysis.py
│   └── export.py
├── outputs/                  # CSV and other generated files
├── requirements.txt          # Project dependencies
├── .gitignore                # Ignored files
└── README.md                 # This file
```

## 🛠️ Customization

* **Tickers:** Modify the `tickers` list in Step 2 of the notebook.
* **Filings Count:** Adjust `count_per_cik` in Step 3.
* **Regex Patterns:** Update `src/parse_exhibits.py` if exhibit naming differs.
* **Keywords:** Change `top_n_keywords` in Step 5 or `assemble_records()`.

## 🤝 Contributing

1. Fork the repo and create a branch.
2. Submit a pull request with your improvements.

---

© 2025 SilentBillionAI | by Karissa Bryant
