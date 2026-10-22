# RetailScope Architecture

## Summary
RetailScope is a read-only analytics dashboard. It retrieves a public dataset at runtime, validates and transforms it in memory, and serves interactive analytics through Streamlit. No raw dataset is committed; no persistent database is required.

## Component flow
```text
UCI Online Retail (public source)
  -> src/data_source.py (retrieval + metadata)
  -> src/validation.py (schema, types, data quality)
  -> src/transformations.py (normalization, classification, derived fields)
  -> src/metrics.py + sql/*.sql (KPIs and SQL views)
  -> src/app_cache.py (Streamlit cache)
  -> Streamlit pages + Plotly charts
```

## Modules
- `src/config.py`: constants and governed definitions.
- `src/exceptions.py`: project-specific errors.
- `src/data_source.py`: sole owner of remote retrieval and source metadata.
- `src/validation.py`: schema checks and quality reports.
- `src/transformations.py`: type coercion, date parsing, row classification.
- `src/metrics.py`: all KPI formulas and filters.
- `src/sql_runner.py`: in-memory DuckDB registration and SQL execution.
- `src/insights.py`: data-driven callouts with suppression rules.
- `src/filters.py`: shared Streamlit filter controls.
- `src/app_cache.py`: cached dataset loading.

## Design rules
- UI does not clean data; all transformations live in importable `src`.
- Row classification is exhaustive: ordinary sale + exception = total rows.
- KPI definitions are centralized and tested.
- Empty results return documented null/placeholder values rather than division-by-zero.
- Filters operate on cached in-memory data, not the source.
