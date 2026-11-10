import pandas as pd

weights = {
    "completeness": 0.20,
    "joinability": 0.25,
    "freshness": 0.15,
    "coverage": 0.15,
    "sales_value": 0.25,
}

sources = [
    {
        "source": "Open Payments",
        "completeness": 5, "completeness_why": "0.2% missing key fields, 0 duplicates",
        "joinability": 5, "joinability_why": "99.8% of payments link to an NPI",
        "freshness": 3, "freshness_why": "Annual release, 2024 data (about 1 year behind)",
        "coverage": 3, "coverage_why": "Only providers who received industry payments",
        "sales_value": 5, "sales_value_why": "Names the device company, product and doctor in one row",
    },
    {
        "source": "Medicare Providers",
        "completeness": 5, "completeness_why": "0% missing key fields, 0 duplicates",
        "joinability": 4, "joinability_why": "100% NPI, but only 77.8% of paid doctors appear",
        "freshness": 3, "freshness_why": "Annual release, 2024 data (about 1 year behind)",
        "coverage": 3, "coverage_why": "Misses NPs and PAs who bill under a supervising doctor",
        "sales_value": 3, "sales_value_why": "Shows patient volume, but no device or company info",
    },
    {
        "source": "NPI Registry",
        "completeness": 5, "completeness_why": "1.0% missing key fields (credential 9.5%)",
        "joinability": 5, "joinability_why": "99.8% of paid doctors found; NPI is the join key",
        "freshness": 4, "freshness_why": "Updated daily, but 44.3% of records unchanged in 5+ years",
        "coverage": 5, "coverage_why": "Every US provider, any insurance",
        "sales_value": 2, "sales_value_why": "Directory only: who and where, no buying signal",
    },
]

df = pd.DataFrame(sources)
df["weighted_score"] = sum(df[c] * w for c, w in weights.items()).round(2)
df = df.sort_values("weighted_score", ascending=False)

print(df[["source"] + list(weights) + ["weighted_score"]].to_string(index=False))
df.to_csv("output/scorecard.csv", index=False)