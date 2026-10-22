# RetailScope: Online Retail Business Analytics
## Detailed Requirements Specification (SRS / PRD)
**Version:** 1.0  |  **Status:** Baseline for implementation  |  **Prepared:** 20 October 2026
**Purpose:** Build a public, portfolio-quality data analytics project to demonstrate end-to-end analyst skills using an online public dataset, SQL, Python, data-quality controls, interactive dashboarding, and clear business recommendations.

> **Baseline decision:** The primary deliverable is a Streamlit web dashboard backed by a runtime-loaded public dataset from UCI and an in-memory DuckDB analytical layer. The dataset is historical, not a live business feed. The project must not depend on a dataset file stored on the developer laptop or committed to GitHub.

## Document control
| Field | Value |
|---|---|
| Project name | RetailScope — Online Retail Business Analytics |
| Version | 1.0 |
| Document type | Product requirements + software requirements specification |
| Primary audience | Hiring managers, recruiters, analytics peers, project owner |
| Target role | Data Analyst / BI Analyst / Reporting Analyst |
| Budget | Free-tier-first; no paid domain or paid dashboard service required |
| Deployment target | Streamlit Community Cloud + public GitHub repository |

## Contents
- 1. Executive summary
- 2. Problem statement and objectives
- 3. Scope and exclusions
- 4. Stakeholders and users
- 5. Dataset and source requirements
- 6. Business questions and analytical use cases
- 7. KPI and metric definitions
- 8. Functional requirements
- 9. Non-functional requirements
- 10. Dashboard requirements
- 11. Data architecture and processing flow
- 12. Repository structure and technology choices
- 13. Data quality, validation and testing
- 14. Deployment and operations
- 15. Acceptance criteria
- 16. Delivery plan and milestones
- 17. Risks and mitigations
- 18. Portfolio and interview outcomes
- 19. Definition of done
- 20. References

## 1. Executive summary
RetailScope is a business analytics portfolio project built around the UCI Online Retail transaction dataset. The app will fetch source data over the internet when the hosted app initializes, validate and transform it, query it through DuckDB in memory, and display interactive analysis in Streamlit. The public GitHub repository will provide SQL, Python source code, tests, documentation, screenshots, and reproducible setup instructions.
The project is intended to demonstrate analyst workflow, not merely chart creation: translating business questions into metrics, reviewing source quality, documenting assumptions, calculating KPIs consistently, interpreting patterns, and communicating caveats. The project will be free-tier-first, but the document does not promise perpetual free availability because providers can change limits or terms.

## 2. Problem statement and objectives
### Problem statement
A recruiter cannot easily evaluate a candidate’s analytical thinking from a list of tools or a static screenshot alone. A useful portfolio project should expose a working analysis, show how data was sourced and cleaned, make metric definitions inspectable, and connect findings to business decisions.
### Objectives
- Build a publicly accessible interactive dashboard with no sign-in required for viewers.
- Demonstrate SQL querying, Python/pandas transformation, data validation, and business intelligence storytelling.
- Use a documented public dataset fetched at runtime rather than a developer-managed local data file.
- Make metric definitions reproducible and prevent inconsistent calculations across charts.
- Explain findings in plain business language and disclose dataset limitations.
- Keep hosting and tooling costs at zero during normal portfolio usage, subject to free-tier constraints.
### Success measures
- A recruiter can open the app URL and understand the project in under two minutes.
- The dashboard provides at least five useful analytical views and several interactive filters.
- Core KPIs agree across cards, charts, tables, and SQL/Python checks.
- The repository contains tests and documentation sufficient for another analyst to reproduce the workflow.
- No dataset file, credentials, or private personal information is committed.

## 3. Scope and exclusions
### In scope
- Online retrieval of UCI Online Retail data through an official UCI source interface or official hosted file.
- Runtime schema validation, data-quality profiling, row classification, and derived analytical fields.
- In-memory DuckDB SQL queries and pandas calculations.
- Interactive Streamlit dashboard with Plotly visualizations, filters, methodology notes, and data-quality reporting.
- Product, time, country, order, and customer-pattern analysis using fields actually present in the dataset.
- Automated tests for important data rules and KPI formulas.
- Public GitHub repository, project README, screenshots, source citations, and free deployment.
### Out of scope
- Real-time sales, current market activity, or ongoing updates from the original retailer.
- Forecasting or machine-learning prediction as a required deliverable.
- Profit margin, cost-of-goods-sold, discount-effectiveness, or net-profit analysis; the source does not provide the required cost/discount fields.
- Inventory-on-hand, marketing campaigns, shipping-cost, or advertising attribution analysis.
- A persistent database, user accounts, private dashboards, or user-generated uploads in the first release.
- Paid Power BI Service, custom domain purchase, paid cloud infrastructure, or paid API keys.
- Public display of raw transaction data or customer-level identifier lists.

## 4. Stakeholders and users
| Stakeholder | Need |
|---|---|
| Recruiter / hiring manager | Quickly inspect evidence of practical analytical ability and communication. |
| Data Analyst peer | Understand data lineage, quality rules, SQL logic, and KPI definitions. |
| Project owner | Improve job prospects, learn from a coherent real-world-like project, and maintain it affordably. |
| Dashboard viewer | Explore performance by date, country, and product without needing local tools. |

### User stories
- As a recruiter, I want a public link that opens directly so I can evaluate the work without installing software.
- As an analyst, I want to inspect the methodology and row-handling rules so I can trust what the KPIs mean.
- As a business viewer, I want to filter by date and country so I can compare performance for a specific period or market.
- As a project maintainer, I want the data loader and calculations separated from the UI so I can test and change them safely.
- As a reviewer, I want source attribution and limitations visible so I can distinguish observed facts from assumptions.

## 5. Dataset and source requirements
### Primary dataset
**Dataset:** UCI Machine Learning Repository — Online Retail. Official source: https://archive.ics.uci.edu/dataset/352/online%2Bretail
The dataset describes transactions from a UK-based non-store online retailer from 1 December 2010 through 9 December 2011, with 541,909 transaction rows listed by UCI. UCI provides an XLSX file of approximately 22.6 MB and documents the license as Creative Commons Attribution 4.0 International (CC BY 4.0). Use the exact source citation and license terms shown on the official UCI page at implementation time.
**Suggested attribution:** Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0.
### Source fields used
| Field | Meaning | Important rule |
|---|---|---|
| InvoiceNo | Invoice identifier; codes beginning with C indicate cancellation | Preserve original text and classify cancellation flag. |
| StockCode | Product identifier | Treat as a label/string, not a numeric measure. |
| Description | Product description | May be missing or inconsistent; never use as the only product key. |
| Quantity | Item quantity on a line | Positive quantities are sale candidates; zero/negative require exception treatment. |
| InvoiceDate | Timestamp of invoice | Parse robustly and record invalid values. |
| UnitPrice | Price per unit, in GBP | Validate positive values for ordinary sales KPIs. |
| CustomerID | Customer identifier | Missing values mean customer-level KPIs cannot include that line. |
| Country | Customer country as recorded in data | Group by source label; do not infer profitability or logistics facts. |
### Online versus live data clarification
“Online data” in this project means the app retrieves a public dataset from the internet at runtime. The source itself is historical and does not update to current retail activity. Do not label the dashboard “live sales”. A future live-data project may use a genuinely updating public API, but that is a separate scope.
### Retrieval and caching rules
- Use the `ucimlrepo` package (dataset ID 352) or a direct link to the official UCI-hosted dataset file. Encapsulate source retrieval in one function so the mechanism can be swapped without rewriting the dashboard.
- Do not commit the downloaded workbook, generated raw data files, or large raw extracts to GitHub.
- Cache only a successful read/normalization result in the hosted app runtime with a reasonable TTL; filters should operate on the cached in-memory data.
- If source retrieval fails, show a helpful unavailable/retry message, and do not silently use stale local files or fabricate data.
- Record retrieval timestamp, source URL, row count, and dataset date range in diagnostics or methodology metadata.
- The app must continue to be honest if the upstream URL, schema, or package changes.

## 6. Business questions and analytical use cases
### 6.1 Sales trend
How does sales value change by day and month? Which periods have the highest and lowest observed sales? Is a trend driven by invoice volume or average invoice value?
### 6.2 Product performance
Which products contribute most to sales value and unit volume? Which eligible products show low volume or low value during the selected period? Is the apparent ranking affected by sparse activity or missing descriptions?
### 6.3 Country performance
Which countries contribute most to sales value, invoices, and identifiable customers? How does the country mix change over time?
### 6.4 Customer behavior
How many identifiable customers purchase more than once? What does invoice frequency look like? Which customer groups appear recently active relative to the dataset snapshot?
### 6.5 Cancellation and data quality
How much data is missing or unusual? How many rows have cancellation invoice codes, non-positive quantities or prices, missing customer IDs, missing descriptions, invalid dates, or exact duplicates?
### 6.6 Business communication
What are three to five evidence-based findings, what might explain them, what cannot be concluded from this dataset, and what further data would be needed?

## 7. KPI and metric definitions
These definitions are a controlled contract. The same logic must be implemented in SQL and Python and documented in the app. If tests reveal source-specific cases that require a revision, update the definitions and README explicitly rather than silently changing a formula.
| KPI | Definition | Caveat |
|---|---|---|
| Sales value (filtered) | Sum of Quantity × UnitPrice for rows classified as ordinary sales (invoice not prefixed with C, Quantity > 0, UnitPrice > 0). | GBP (£); label as historical sales value, not profit or audited net revenue. |
| Orders / invoices | Distinct non-cancellation InvoiceNo among ordinary sale rows. | An invoice can contain multiple line items; never count rows as orders. |
| Units sold | Sum of positive Quantity over ordinary sales rows. | Exclude return/cancellation/exception rows from this KPI and report them separately. |
| Average order value (AOV) | Sales value ÷ distinct eligible invoices for the same filters. | Display as undefined / — when order count is zero. |
| Active customers | Count of distinct non-null CustomerID among ordinary sales rows. | The dataset has missing CustomerID values; show coverage. |
| Repeat customers | Customers with at least two distinct eligible invoices in the analysis window. | Repeat-customer share = repeat customers ÷ identifiable active customers; do not treat missing IDs as one customer. |
| Cancellation/return exception value | Sum of absolute Quantity × UnitPrice for rows with numeric amounts flagged as cancellation, non-positive quantity, or non-positive unit price; break out reason where possible. | Keep separate from sales value; invalid-date-only rows should be counted in data quality, not added to exception value. Do not automatically subtract without a validated matching method. |
| Product sales ranking | Sales value and units, aggregated by StockCode (Description shown as a label). | StockCode is the stable product identifier; descriptions can be missing or inconsistent. |
| Country sales | Sales value, eligible invoices, and identifiable active customers grouped by Country. | Use full country name. Do not infer profit, shipping location, or market share. |
| RFM segments | Recency = days since last observed eligible invoice as of one day after the dataset maximum timestamp; Frequency = distinct eligible invoices; Monetary = sales value. | Historical snapshot only; document scoring/quantiles and exclude unknown CustomerID. |
### Row classification baseline
- `is_cancellation_invoice`: InvoiceNo begins with C after trimming and normalizing case.
- `is_ordinary_sale`: not a cancellation invoice AND Quantity > 0 AND UnitPrice > 0 AND InvoiceDate parsed successfully.
- `is_exception`: cancellation invoice OR Quantity <= 0 OR UnitPrice <= 0 OR unparseable date; record a reason code where possible.
- Rows with missing CustomerID or Description may still contribute to eligible sales value if otherwise valid; they are excluded only from customer- or description-dependent metrics as relevant.
- Exact duplicate rows are flagged for review, not automatically removed in the first release. Removal would risk deleting legitimate repeated line items.
- Do not compute profit, margin, discount impact, or a definitive net revenue measure because relevant cost, discount, and cancellation-matching information is not present.
### Calculation governance
- Each KPI must be implemented in a centralized calculation module and exposed through named functions or SQL views.
- Date filters must use inclusive start/end dates and make timezone/date interpretation clear.
- Empty denominators return a documented null/“—” rather than infinity or an arbitrary zero.
- Rounding is presentation-only. Use unrounded values for subsequent calculations.
- GBP is the reported currency because UnitPrice is defined in sterling. Do not convert to INR unless a dated exchange-rate source and conversion scope are formally added.

## 8. Functional requirements
| ID | Requirement | Priority | Acceptance evidence |
|---|---|---|---|
| FR-01 Online source retrieval | The application shall retrieve the Online Retail dataset at runtime from the UCI Machine Learning Repository using the official dataset interface or official hosted file. | Must | App loads without a user-uploaded or repository-committed dataset. |
| FR-02 Attribution | The application and README shall credit the dataset creator/source and identify the CC BY 4.0 license. | Must | Source and license attribution are visible in the app methodology page and README. |
| FR-03 Cache and resilience | The loader shall cache a successful data load for a limited period and show a clear error state if the source is unreachable. | Must | Repeated filter changes do not re-download the source; a failed source request does not produce fabricated results. |
| FR-04 Schema validation | The app shall validate required source fields and types before calculation. | Must | A missing or renamed required field raises a readable diagnostic. |
| FR-05 Data-quality audit | The app shall quantify missing values, exact duplicate rows, non-positive quantities/prices, cancellation invoice codes, invalid timestamps, and missing descriptions/customer IDs. | Must | A Data Quality page/table reports counts and percentages by issue. |
| FR-06 Explicit row classification | The pipeline shall classify ordinary sale lines separately from cancellation/return/exception lines using documented rules. | Must | Every row receives a documented classification; rows are not silently discarded. |
| FR-07 KPI definitions | All displayed KPIs shall use central, tested definitions that are also documented in the Methodology page. | Must | KPI values remain consistent across charts and tables for identical filters. |
| FR-08 Overview dashboard | The app shall show headline KPIs and monthly sales trend for the selected filter context. | Must | The Overview page contains clearly labelled KPIs, a time series, and a brief insight summary. |
| FR-09 Time analysis | The app shall support day/month trend analysis and comparison of periods where enough observations exist. | Must | Date filters update the time series and summary consistently. |
| FR-10 Product analysis | The app shall show leading products by sales value and quantity, plus a low-performing product view with minimum-activity context. | Must | Product rankings respect filters and clearly show the metric used. |
| FR-11 Geographic analysis | The app shall compare countries by sales value, orders, and customers where customer IDs are available. | Must | Country charts and tables use selected filters and note that the UK is the source retailer location context, not every buyer location. |
| FR-12 Customer analysis | The app shall report customer count, repeat-customer share, order-frequency patterns, and RFM-style segments using identifiable customer IDs only for aggregate calculations. | Must | No raw customer-level export or customer ID leaderboard is exposed in the public app. |
| FR-13 Interactive filters | The app shall provide date range, country, top-N, and customer-ID availability filters when meaningful. | Must | All relevant visuals respond to filters and show the current selection. |
| FR-14 SQL demonstration | The repository shall include readable SQL queries/views for the core business questions, using DuckDB SQL over the runtime-loaded data. | Must | Queries run against the normalized in-memory data and have documented expected outputs. |
| FR-15 Python pipeline | The code shall separate source loading, validation, transformation, KPI computation, and presentation logic. | Must | Loading/cleaning/KPI modules can be imported and tested independently of Streamlit UI. |
| FR-16 Business insights | The app shall surface concise insight statements based on computed values, not hard-coded conclusions. | Must | Insight text changes with filters or is clearly identified as static methodology guidance. |
| FR-17 Methodology and caveats | The app shall explain dataset date coverage, metric rules, missing-data treatment, currency, and limitations. | Must | A reviewer can tell that values are historical and cannot be interpreted as current performance. |
| FR-18 Public deployment | The app shall be deployable from a public GitHub repository to Streamlit Community Cloud without a paid domain or API key. | Must | A public URL opens the app and no secrets are required. |
| FR-19 README portfolio story | The README shall include project objective, data source/citation, architecture, KPI definitions, screenshots, findings, limitations, deployment link, and how to run tests. | Must | A recruiter can understand the project without reading every source file. |
| FR-20 Automated tests | The project shall contain tests for row classification, KPI calculations, date parsing, and edge cases. | Must | Tests pass locally or in the chosen automated test workflow. |
| FR-21 Usability and accessibility | Charts shall have descriptive titles, axis labels, readable formats, and non-colour-only interpretation where practical. | Should | Dashboard remains understandable on a common desktop viewport and narrow screens. |
| FR-22 Downloadable summaries | The app may provide a download of aggregated filtered results, without exposing raw customer identifiers. | Should | Downloads contain only documented aggregate measures and selection metadata. |
| FR-23 Optional portfolio site | A lightweight GitHub Pages landing page may link to the live app and repository. | Could | Page is static and contains no secrets or user-data collection. |

## 9. Non-functional requirements
| ID | Requirement |
|---|---|
| NFR-01 Performance | On the target dataset size, initial loading and transformation should complete within a reasonable free-tier budget; use caching and avoid re-reading the source on each interaction. |
| NFR-02 Reliability | The app must handle source outage, schema drift, malformed dates, and empty filter selections without crashing into an unhandled traceback. |
| NFR-03 Reproducibility | A clean checkout plus documented dependencies shall reproduce the analysis; versions of major libraries should be pinned or bounded. |
| NFR-04 Security | No API keys, passwords, private tokens, or personal credentials are needed. Do not place secrets in GitHub, logs, screenshots, or app output. |
| NFR-05 Data privacy | Display aggregate analysis only. Do not provide raw-level customer exports, exposed customer-ID lists, or personal details. |
| NFR-06 Transparency | Metric labels must disclose whether cancelled/return rows are excluded, separately reported, or used in a signed adjustment. |
| NFR-07 Cost | The initial production-like demo should use free services only; usage limits, hibernation, availability, and terms can change and are not guaranteed. |
| NFR-08 Portability | The core analysis functions must run outside the Streamlit UI for unit testing and local development. |
| NFR-09 Maintainability | Use a clear folder structure, small functions, meaningful names, comments for non-obvious business rules, and no monolithic app file. |
| NFR-10 Accessibility | Avoid tiny text, ambiguous colours, truncated labels, and charts without accessible titles or explanatory text. |

## 10. Dashboard requirements
### Global experience
- Use a clear title, one-sentence business purpose, source/date coverage, and a visible “historical dataset — not live sales” disclosure.
- Provide global filters for date range and country. Provide top-N and customer-ID-availability controls where relevant.
- Show active filters and a clear reset option. Empty results must produce a friendly message.
- Use readable currency/count formats, informative hover details, descriptive axis labels, and responsive layout.
- Keep source attribution and metric definitions accessible from a Methodology/About area.
### Page 1 — Executive overview
- KPI cards: eligible sales value (GBP), eligible invoices, units sold, identifiable active customers, repeat-customer share.
- Monthly trend chart: sales value over time; optionally pair with invoice count as a separate view to avoid confusing units.
- Country contribution chart or ranked table (top countries).
- Product leaders table or chart based on sales value.
- Automated insight callouts based on computed period-over-period values, with a rule to suppress claims when data is insufficient.
### Page 2 — Sales trends
- Daily and monthly time-series view.
- Break out invoice count and average order value to separate volume from order-size effects.
- Support a selected time window; no interpolation or projections presented as actual observations.
- If comparing periods, label absolute and percentage changes and handle zero prior-period values safely.
### Page 3 — Product analysis
- Top products by sales value and by units, selected separately.
- A low-activity table with selected threshold/period clearly stated; do not call a product “unprofitable” because no cost field exists.
- Use StockCode as the key and Description as a display label.
- No product categories are assumed because the source schema does not include an authoritative category field.
### Page 4 — Geographic analysis
- Rank countries by eligible sales value, invoices, and identifiable active customers.
- Provide contribution percentage of selected-filter sales where denominator is non-zero.
- A map is optional and not a release blocker; only add it if country geocoding is correct and does not distract from business interpretation.
### Page 5 — Customer analysis
- Show identified customer count, repeat-customer share, orders-per-customer distribution, and RFM segment counts.
- Use a documented snapshot date based on the dataset max timestamp plus one day for recency calculations.
- Do not expose raw customer IDs, raw customer transaction histories, or customer-level downloads in the public dashboard.
- Make missing CustomerID coverage visible to explain why customer metrics are based on a subset.
### Page 6 — Data quality and methodology
- Report source row count, parsed row count, date range, missing values, cancellation rows, negative/zero quantities, non-positive prices, missing descriptions, missing customer IDs, and exact duplicates.
- Explain which rows contribute to ordinary sale KPIs and which are excluded or separately reported.
- Show that exclusions are explicit and not invisible data loss.
- Include dataset citation, license, definitions, version/date of last successful retrieval, and limitations.

## 11. Data architecture and processing flow
```text
UCI Online Retail (public hosted source)
             | HTTPS/runtime retrieval
             v
      Source loader + cache
             | schema checks
             v
    Validation / classification layer
             | normalized in-memory table
             v
      DuckDB SQL + pandas KPIs
             | results / aggregates
             v
      Streamlit + Plotly dashboard
             |
             v
 Streamlit Community Cloud public URL

Public GitHub repository: application, SQL, tests, docs; no raw dataset and no secrets.
```
### Design constraints
- No persistent database is required in release 1. DuckDB should operate in memory; the app must not depend on a local `.db` file surviving a redeploy.
- The dashboard UI must not perform data cleaning inline. Transformations belong in importable modules with unit tests.
- Use pandas for data preparation and grouped analysis where sensible; use DuckDB SQL to demonstrate querying, joins/CTEs/window functions or equivalent analyst techniques over the loaded dataset.
- Use Plotly charts where interactive tooltips and zoom add value; avoid charts that do not answer a business question.
- The source loader should have a small and documented timeout/retry policy. Avoid endless retries that keep a free hosting worker busy.

## 12. Repository structure and technology choices
### Proposed repository layout
```text
retailscope/
├── app.py
├── pages/
│   ├── 1_Sales_Trends.py
│   ├── 2_Product_Analysis.py
│   ├── 3_Country_Analysis.py
│   ├── 4_Customer_Analysis.py
│   └── 5_Data_Quality_Methodology.py
├── src/
│   ├── data_source.py
│   ├── validation.py
│   ├── transformations.py
│   ├── metrics.py
│   ├── sql_runner.py
│   └── insights.py
├── sql/
│   ├── 01_sales_overview.sql
│   ├── 02_product_performance.sql
│   ├── 03_country_performance.sql
│   ├── 04_customer_rfm.sql
│   └── 05_data_quality.sql
├── tests/
│   ├── test_row_classification.py
│   ├── test_metrics.py
│   └── test_data_quality.py
├── docs/
│   ├── data_dictionary.md
│   └── methodology.md
├── assets/
│   └── screenshots/
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE (project code license; separate from dataset license)
```
### Technology decisions
| Component | Choice | Reason |
|---|---|---|
| Data source | UCI Online Retail + `ucimlrepo` or official file endpoint | Recognized research repository, openly licensed, and no API key needed. |
| Language | Python | Main implementation language and broad analyst relevance. |
| Data wrangling | pandas | Transparent cleaning, data typing, grouping, and validation. |
| SQL engine | DuckDB in-memory | Demonstrates SQL without a managed database or persistence cost. |
| Dashboard | Streamlit Community Cloud | Public shareable Python web app with free deployment documented by provider. |
| Charts | Plotly | Interactive filters, hover details, and readable business charts. |
| Tests | pytest | Reproducible validation of transformation and metric logic. |
| Source control | Public GitHub repository | Code review, history, and recruiter-friendly portfolio evidence. |
### Free-tier assumptions
Streamlit Community Cloud currently documents free app deployment from GitHub. Apps can sleep after inactivity and resources/limits can change. Public GitHub is needed for the simplest deployment path. Do not promise continuous uptime. A custom domain, paid database, private hosting, or Power BI Service sharing is not required for release 1.

## 13. Data quality, validation and testing
### Required data checks
- Required fields exist: InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, and Country; Description and CustomerID are expected but may contain missing values.
- InvoiceNo, StockCode, and Country are read as identifiers/categories, not inferred numeric measures.
- InvoiceDate parses to a consistent datetime type; invalid rows are counted and excluded from time-dependent ordinary sale measures.
- Quantity and UnitPrice numeric conversion failures are counted and not silently coerced to meaningful values.
- Missing Description and CustomerID counts are reported before filtering.
- Exact duplicate rows are counted and sampled internally for diagnostic purposes; not automatically deleted.
- Cancellation invoice prefixes are handled case-insensitively after trimming.
- For ordinary sales, Quantity and UnitPrice must both be positive. Exceptional rows are retained in the quality dataset and classified.
- Post-transformation row counts reconcile: ordinary sales + exception rows + invalid rows = total loaded rows, using mutually exclusive classification order.
- The maximum/minimum invoice date in the loaded data match the values reported in the app after parsing.
### Minimum automated tests
- Cancellation prefix: `C`/`c` invoice codes are correctly flagged.
- Negative or zero quantity and non-positive unit price are not ordinary sale rows.
- Missing CustomerID does not inflate active or repeat customer counts.
- A small hand-built fixture produces the expected sales value, invoice count, units, and AOV.
- A zero-invoice period returns a safe empty/null KPI instead of division by zero.
- Date filters include both endpoints as documented and exclude out-of-range rows.
- Product aggregation groups by StockCode even when descriptions vary or are missing.
- All user-facing KPI functions return consistent results for equivalent filters.
- Data loading failure results in a friendly error state and no mock data.

## 14. Deployment and operations
### Deployment steps
- Create a public GitHub repository named `retailscope-online-retail-analytics` or a similarly clear name.
- Add the application source, SQL files, tests, requirements file, README, and `.gitignore`. Do not upload the raw XLSX dataset.
- Run tests and a local smoke test with internet access before deployment.
- Open Streamlit Community Cloud, connect the public repository, select the entry-point app file, and deploy.
- Configure a stable descriptive app subdomain if available; use the app URL in the repository README and portfolio profiles.
- After deployment, test the public app in a private/incognito browser and on a narrow/mobile viewport.
- Capture genuine screenshots of the deployed app and keep them updated after significant UI changes.
- Inspect cloud logs after any deployment or data-source failure.
### Operational behavior
- At startup, load and validate the dataset once per cache lifetime.
- On filters, calculate from the in-memory prepared dataset; do not call the source repeatedly.
- On source/schema failure, show a non-technical error with the source link and retry guidance; log diagnostic details without secrets.
- When the app sleeps due to hosting policy, users may need to wait for wake-up; document that hosting is a free-tier demo.
- No scheduled refresh is required because the source dataset is historical and static.

## 15. Acceptance criteria
- [ ] AC-01: A fresh deployment can retrieve data from UCI without a local dataset file or API key.
- [ ] AC-02: The raw dataset is not present in the public repository or packaged app assets.
- [ ] AC-03: The source attribution and CC BY 4.0 reference appear in the dashboard and README.
- [ ] AC-04: Required columns and datatypes are validated, and failures are reported clearly.
- [ ] AC-05: Cancellation/exception rows are identified and do not silently flow into ordinary-sale KPIs.
- [ ] AC-06: Sales value, invoices, units, AOV, customer count, repeat-customer share, product ranking, and country ranking have documented formulas.
- [ ] AC-07: Dashboard filters update all relevant metrics and visualizations consistently.
- [ ] AC-08: Time series, product analysis, country analysis, customer analysis, and data-quality/methodology views are available.
- [ ] AC-09: No profit or discount claims are displayed because the source lacks the needed data.
- [ ] AC-10: No raw customer ID table, raw customer transaction export, secret, or credential is visible in app/repository.
- [ ] AC-11: Unit tests cover classification and key calculations and pass in a clean environment.
- [ ] AC-12: README has business context, project structure, reproducibility steps, app URL, screenshots, KPIs, limitations, and source citation.
- [ ] AC-13: The public app opens from a signed-out browser and provides a meaningful page when there are no rows for a chosen filter.
- [ ] AC-14: The app explicitly states that data represents 2010–2011 transactions and is not live/current data.

## 16. Delivery plan and milestones
| Phase | Work package | Exit condition |
|---|---|---|
| P0 — Repository setup | Create repo, Python environment/dependencies, folder structure, `.gitignore`, README skeleton. | Clean project runs a minimal app; no data file is committed. |
| P1 — Source and profiling | Implement online UCI loader, cache, schema validation, data-quality report. | The app reports source row count, date range, missing values, cancellations, and exceptions. |
| P2 — Analytical rules | Implement row classification, central KPI module, DuckDB SQL files, unit tests. | SQL and Python calculations reconcile on test fixtures. |
| P3 — Dashboard MVP | Create overview, trends, products, countries, customers, and methodology/data-quality pages. | Core charts and filters work on the hosted data. |
| P4 — Insights and polish | Add evidence-based insight callouts, labels, loading/error states, responsive layout, chart details. | Dashboard is understandable without code knowledge. |
| P5 — Publish | Deploy to Streamlit Community Cloud, test public URL, add screenshots and portfolio README. | Public app and repository pass acceptance checklist. |
| P6 — Interview preparation | Create a one-page case study, 5-minute walkthrough, STAR-style explanation of decisions and limitations. | Project can be presented clearly in an interview. |
Suggested workflow: deliver one testable phase at a time. A likely sequence is 6–8 focused sessions, but the actual time depends on troubleshooting and polish; this is a planning guide, not a time guarantee.

## 17. Risks and mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| UCI endpoint/package changes | App cannot load data after deployment. | Isolate the loader; test official source; provide readable errors and a documented alternative official UCI download endpoint. |
| Dataset is historical | Recruiter misinterprets it as current live sales. | Show time coverage and “historical—not live” disclosure on overview and methodology pages. |
| Ambiguous cancellations/returns | Sales measures can be misleading. | Separate ordinary sales from exceptions; publish explicit definitions; avoid automatic net revenue claims until matching logic is validated. |
| Missing CustomerID | Customer metrics do not represent all transactions. | Show coverage rates and base customer metrics only on identifiable customers. |
| False profit claims | Business analysis appears unreliable. | Explicitly exclude profit, margin, and discount analysis without cost/discount fields. |
| Free hosting limits/hibernation | Slow or sleeping dashboard. | Use cache, moderate memory, avoid needless compute, and disclose free hosting behavior. |
| Large workbook / memory pressure | App fails during load or transformation. | Avoid duplicate copies where possible, select relevant fields, cache carefully, and inspect memory usage. |
| Overly complex scope | Project remains unfinished. | Prioritize six core pages and acceptance criteria; defer maps, predictive models, and extra data sources. |
| Public repository accident | Credentials or private material leaked. | No secrets needed; use `.gitignore`; check staged files and repository history before public push. |

## 18. Portfolio and interview outcomes
The final project should communicate the following competencies through visible evidence:
- SQL: filtering, grouping, joins where relevant, CTEs, window functions, ranking, date aggregation, and quality queries.
- Python: loading remote data, parsing, transformation, reusable functions, exception handling, testing, and pandas aggregation.
- Business intelligence: KPI selection, filter design, chart choice, drill-down, and clear explanations.
- Data governance: source citation, lineage, data-quality checks, metric definitions, and explicit limitations.
- Communication: concise business findings, what action they suggest, and what additional data would be required to validate a causal explanation.
- Engineering habits: Git history, repository structure, dependency management, automated tests, deployment, and documentation.
### Required project story
The README and interview narrative should answer: (1) What business questions did you choose and why? (2) What was challenging about source quality? (3) How did you define sales and treat cancellations? (4) How did you validate SQL/Python results? (5) What are the strongest findings? (6) What cannot be concluded? (7) What would you do next with additional data? Findings must be populated only after analysis is run; do not pre-write invented numbers or conclusions.

## 19. Definition of done
- [ ] All Must-priority functional requirements are satisfied.
- [ ] All acceptance checks are completed or explicitly listed as known limitations.
- [ ] The public app and repository links are valid and included in README.
- [ ] Source attribution/license is present.
- [ ] SQL and Python results reconcile against test fixtures and spot checks.
- [ ] Dashboard shows no unlabelled mock values, misleading live-data language, profit claims, or customer ID exposures.
- [ ] The raw source data is fetched at runtime and is not committed to Git.
- [ ] A recruiter-facing project walkthrough and methodology summary are ready.

## 20. References
1. UCI Machine Learning Repository, Online Retail dataset: https://archive.ics.uci.edu/dataset/352/online%2Bretail
2. Dataset citation: Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.
3. Streamlit Community Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
4. Streamlit app deployment guide: https://docs.streamlit.io/get-started/tutorials/create-an-app
5. Streamlit Community Cloud app resource and hibernation notes: https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
6. GitHub Pages limits (optional portfolio landing page): https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
7. Tableau Public (optional alternative dashboard platform): https://www.tableau.com/products/public
8. Looker Studio (optional alternative): https://lookerstudio.google.com/about
