# Requirements Analysis and Suggestions

## Review result
The DOCX and MD versions of the requirements describe the same specification. No substantive content difference was found beyond document formatting and Markdown syntax. Both are retained for traceability.

## Strengths
- Clear portfolio story targeted at analyst roles.
- Controlled KPI definitions and row-classification baseline.
- Explicit exclusions prevent unsupported profit or forecast claims.
- Strong testing, reproducibility, and public-accessibility expectations.
- Reasonable free-tier-first hosting strategy.

## Gaps / ambiguities found
1. Date format: UCI metadata is written in day-first European notation, while the downloaded export uses month-first slash dates. Parsing must be reconciled (the project uses inference and records the resulting range).
2. `is_exception` classification ordering: the specification defines the logical condition but not the exact reason-code precedence. The implementation uses cancellation, invalid date, invalid type, non-positive quantity, then non-positive price.
3. "Repeat customers" and RFM use identifiable CustomerID only; the specification leaves the RFM quantile method open. The implementation uses quintile scores and simple named segments.
4. The specification requests DuckDB SQL demonstration. The implementation registers a view with original source fields plus normalized classification, and includes five SQL files.
5. Product "low-performing" thresholds are not numerically defined in the requirements; the implementation uses a units threshold of 50 and documents it.

## Suggestions
1. Add a synthetic fixture in tests so tests do not depend on the remote source.
2. Use a stable Streamlit subdomain after deployment and put the live link in the README.
3. Add GitHub Actions for pytest and compileall before the first public release.
4. Capture real screenshots of the deployed six pages and add them to assets/screenshots.
5. If interview reviewers ask for deeper analysis, add customer cohort retention and cancellation matching as a documented follow-up project, not release 1.
6. Consider a static GitHub Pages landing page only after the main app and README are complete.
