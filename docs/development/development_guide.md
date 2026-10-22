# RetailScope Development Guide

## Repository name and professional project name
- Repository slug: `retailscope-online-retail-analytics`
- Product/project name: **RetailScope — Online Retail Analytics Dashboard**

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Quality workflow
```bash
pytest
python -m compileall app.py pages src tests
```

## Coding standards
- Keep functions small and named for the business concept they implement.
- All KPI formulas belong in `src/metrics.py`.
- Row classification rules belong in `src/transformations.py`.
- UI pages should only render cached results and call metric functions.
- Add or update tests for every formula or classification change.

## Performance and hosting
- Dataset loading is cached for six hours.
- Avoid repeated remote calls while filters change.
- Do not commit raw XLSX/CSV extracts, logs, or credentials.
- Streamlit Community Cloud may sleep; document as a free-tier limitation.

## Deployment checklist
1. Run `pytest`.
2. Run the app locally with internet access.
3. Verify public source loads from a clean state.
4. Deploy `app.py` from a public GitHub repository.
5. Test in an incognito browser and on a narrow viewport.
