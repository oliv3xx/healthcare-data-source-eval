# Which Healthcare Dataset Should We Add First?

**Question:** A medtech sales team wants to find Kentucky providers to target for their devices. We already have FDA 510(k) clearance data. Which public dataset should we add next?

## Recommendation
Add **CMS Open Payments** first, and use the **NPI Registry** as the lookup layer that ties sources together. Hold **Medicare** for phase 2.

## Why
- Open Payments is the only source that connects a device company, a product, and a specific provider in one row. That's the closest thing to a buying signal in public data.
- It's clean: 0.2% missing key fields, 0 duplicates, and 99.8% of payments link to an NPI.
- The NPI Registry found 99.8% of those providers and covers everyone regardless of insurance. It has no sales signal on its own, but every other source joins on it.
- Medicare matched only 77.8% of paid providers. The gap is mostly nurse practitioners and physician assistants. Device companies clearly pay them, but they often bill under a supervising doctor, so they don't show up in Medicare as their own provider.
- All three sources were clean, so data quality wasn't the deciding factor. Sales value and joinability were.

## Scorecard
| Source | Completeness | Joinability | Freshness | Coverage | Sales Value | Weighted |
|---|---|---|---|---|---|---|
| Open Payments | 5 | 5 | 3 | 3 | 5 | **4.40** |
| NPI Registry | 5 | 5 | 4 | 5 | 2 | **4.10** |
| Medicare Providers | 5 | 4 | 3 | 3 | 3 | **3.65** |

Weights: joinability and sales value 25% each, completeness 20%, freshness and coverage 15% each.

## Risks
- Open Payments and Medicare both run about a year behind (2024 data).
- 44.3% of NPI records haven't been updated in 5+ years, so addresses need a second check before reps rely on them.
- This used a 5,000-row sample of Kentucky device payments. A full-state pull should come next.

## Cost
All three are free public datasets, so the cost is engineering time. Each one took a single Python script to pull.

## Next Steps
1. Pull all Kentucky device payments, not just a sample.
2. Match Open Payments manufacturer names to 510(k) applicants from the FDA device pipeline.
3. Revisit Medicare using the "by Provider and Service" version, which includes procedure codes.