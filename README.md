# Healthcare Data Source Evaluation

Compares three free CMS datasets (Open Payments, Medicare Physician & Other Practitioners, NPI Registry) to decide which one a medtech sales team should add first. Read the full business case in [memo.md](memo.md).

## Results
- 26,000+ records pulled from 3 public APIs for Kentucky
- 77.8% of providers paid by device companies matched across all 3 sources by NPI
- Recommendation: add Open Payments first (weighted score 4.40 of 5)

## How It Works
| Script | What it does |
|---|---|
| `scripts/fetch_open_payments.py` | Pulls 2024 Kentucky device payments from the Open Payments API |
| `scripts/fetch_medicare.py` | Pulls all Kentucky Medicare providers from data.cms.gov |
| `scripts/fetch_npi.py` | Looks up each paid provider in the NPI Registry |
| `scripts/profile_data.py` | Measures missing fields, duplicates, NPI coverage and date range |
| `scripts/join_test.py` | Measures how well the sources match on NPI |
| `scripts/scorecard.py` | Scores each source and ranks them |

## Run It
pip install -r requirements.txt
python scripts/fetch_open_payments.py
python scripts/fetch_medicare.py
python scripts/fetch_npi.py
python scripts/profile_data.py
python scripts/join_test.py
python scripts/scorecard.py

## Tools
Python, pandas, requests, REST APIs