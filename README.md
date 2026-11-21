# Investment Data Hub
## Independent Financial Data Management Product Case Study

An interactive Streamlit prototype exploring how an investment firm could ingest, standardise, validate, master and distribute investment reference and transactional data.

**Important:** This is an independent portfolio project. It is not affiliated with, endorsed by, or a replica of Arcesium or Opterra. All records are synthetic. It does not connect to live vendor feeds or production systems.

## Problem
Investment firms receive security, pricing and transaction data from multiple systems and providers. Inconsistent identifiers, formats, timestamps and source reliability can create manual exceptions and reduce confidence in downstream reporting.

## Features
- Security master with identifier cross-references
- Multi-vendor price comparison and source priority
- Price freshness checks and no-eligible-price warning
- Exception workbench with severity, status, owner and suggested action
- Transaction workbench with filters
- Illustrative data lineage
- Executive operational dashboard
- Product requirements, user stories, UAT and roadmap documentation

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Then open the local URL shown in the terminal (usually http://localhost:8501).

## Repository structure
```text
financial-data-hub/
├── app.py
├── data/
├── docs/
├── tests/
├── requirements.txt
└── README.md
```

## Product positioning
Designed as a product case study to demonstrate product discovery, requirements definition, workflow design, data quality thinking and UAT planning. Explain separately what is documented, what is implemented in the prototype, and what remains a future production capability.

## Future enhancements
Persistent exception workflow, configurable rules, upload and schema mapping, role-based access, maker-checker approval, database/API layer, historical reference data, corporate actions and CI automation.

## License
MIT.
