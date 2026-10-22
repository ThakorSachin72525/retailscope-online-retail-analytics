# Methodology

See the Data Quality and Methodology page in the app and the KPI definitions in the requirements specification. Key rules:

- Ordinary sale: not cancellation, Quantity > 0, UnitPrice > 0, valid timestamp.
- Exception rows are retained and reported by reason.
- Exact duplicates are flagged, not removed.
- Customer metrics use identifiable CustomerID values only.
- Product ranking uses StockCode, with Description as a display label.
- RFM snapshot date is one day after the dataset maximum timestamp.
- Currency is GBP (£).
