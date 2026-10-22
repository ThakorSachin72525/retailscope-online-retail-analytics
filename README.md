# RetailScope — Online Retail Analytics Dashboard

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-community%20cloud-FF4B4B.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](./tests)

RetailScope is a portfolio-quality business analytics project built on the public **UCI Online Retail** dataset. It retrieves the dataset at runtime, validates and classifies every row, calculates consistent KPIs in Python and DuckDB SQL, and presents the results in an interactive Streamlit dashboard.

- Live app: `ADD_STREAMLIT_APP_URL_HERE`
- Repository: `https://github.com/ThakorSachin72525/retailscope-online-retail-analytics`

## Project objective
Help a recruiter or reviewer understand the project in under two minutes while exposing real analyst workflow: business questions, source-quality review, metric contracts, SQL/Python implementation, tests, and limitations.

## Data source and citation
- Dataset: UCI Machine Learning Repository — Online Retail
- Official source: https://archive.ics.uci.edu/dataset/352/online%2Bretail
- Attribution: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.
- License: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Coverage: December 2010 to December 2011 UK-based non-store online retailer transactions.
- The app fetches data at runtime; no dataset file is committed.

## Business questions
1. How does sales value change by day and month?
2. Which products and countries drive sales value and units?
3. How many identifiable customers purchase more than once?
4. What do invoice frequency and RFM-style segments look like?
5. How much data is missing, cancelled, or exceptional?

## KPI definitions
- Sales value (filtered): sum of Quantity × UnitPrice for ordinary sale rows (GBP).
- Orders / invoices: distinct non-cancellation InvoiceNo among ordinary sale rows.
- Units sold: sum of positive Quantity over ordinary sale rows.
- Average order value: sales value ÷ distinct eligible invoices.
- Active customers: distinct non-null CustomerID among ordinary sale rows.
- Repeat-customer share: repeat customers ÷ identifiable active customers.
- Cancellation/exception value: separate amount for cancellation/non-positive rows.
- Product ranking groups by StockCode, with Description as a display label only.
- Country metrics group by the recorded Country label.

## Architecture
```text
UCI source -> src/data_source.py -> src/validation.py -> src/transformations.py
-> src/metrics.py + sql/*.sql -> Streamlit + Plotly
```

## Repository structure
```text
retailscope-online-retail-analytics/
├── app.py
├── pages/
├── src/
├── sql/
├── tests/
├── docs/
├── assets/screenshots/
├── .gitignore
├── requirements.txt
└── README.md
```

## How to run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Internet access is required for the first successful load.

## How to run tests
```bash
pytest
python -m compileall app.py pages src tests
```

## Screenshots
Add genuine deployed-app screenshots to `assets/screenshots/` after deployment.

## Findings
Findings are intentionally not pre-written. Run the dashboard and then populate this section with three to five evidence-based findings, possible explanations, caveats, and required follow-up data.

## Limitations
- Dataset is historical (2010–2011) and not live retail activity.
- No cost, discount, margin, or profit fields; profit claims are out of scope.
- Cancelled/return lines are reported separately rather than automatically netted.
- Customer metrics describe only rows with an identifiable CustomerID.
- Free-tier hosting may sleep after inactivity.

## Methodology
See `docs/methodology/methodology.md`, `docs/requirements/requirements.md`, and the Data Quality and Methodology page in the app.

## License
Project code: MIT License. Dataset: CC BY 4.0; see source citation above.
