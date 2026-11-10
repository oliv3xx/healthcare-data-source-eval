import pandas as pd

op = pd.read_csv("data/open_payments_ky.csv", dtype=str)
mc = pd.read_csv("data/medicare_ky.csv", dtype=str)
npi = pd.read_csv("data/npi_registry_ky.csv", dtype=str)

op_npis = set(op["covered_recipient_npi"].dropna())
mc_npis = set(mc["Rndrng_NPI"])
npi_found = npi[npi["found"] == "True"]
reg_npis = set(npi_found["npi"])

def pct(part, whole):
    return round(len(part) / len(whole) * 100, 1)

results = {
    "op_doctors": len(op_npis),
    "pct_op_in_medicare": pct(op_npis & mc_npis, op_npis),
    "pct_op_in_npi_registry": pct(op_npis & reg_npis, op_npis),
    "pct_op_in_all_three": pct(op_npis & mc_npis & reg_npis, op_npis),
}

ky = npi_found[npi_found["practice_state"] == "KY"]
results["pct_npi_practice_in_ky"] = pct(ky, npi_found)

updated = pd.to_datetime(npi_found["last_updated"], errors="coerce")
cutoff = pd.Timestamp.today() - pd.DateOffset(years=5)
results["pct_npi_not_updated_5yrs"] = round((updated < cutoff).mean() * 100, 1)

for k, v in results.items():
    print(f"{k}: {v}")
pd.DataFrame([results]).to_csv("output/join_results.csv", index=False)

not_in_mc = op[op["covered_recipient_npi"].isin(op_npis - mc_npis)]
not_in_mc = not_in_mc.drop_duplicates("covered_recipient_npi")
print("\nTop specialties paid by device companies but NOT in Medicare:")
print(not_in_mc["covered_recipient_specialty_1"].value_counts().head(5).to_string())