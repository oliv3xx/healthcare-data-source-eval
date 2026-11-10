import pandas as pd

def profile(df, source, key_cols, id_cols, npi_col, date_col=None):
    result = {"source": source, "rows": len(df), "columns": df.shape[1]}
    result["pct_missing_key_fields"] = round(df[key_cols].isna().mean().mean() * 100, 1)
    result["duplicate_rows"] = int(df.duplicated(subset=id_cols).sum())
    result["pct_rows_with_npi"] = round(df[npi_col].notna().mean() * 100, 1)
    result["unique_npis"] = int(df[npi_col].nunique())
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        result["earliest_date"] = dates.min().date()
        result["latest_date"] = dates.max().date()
    else:
        result["earliest_date"] = None
        result["latest_date"] = None

    print(f"\n--- {source} ---")
    for k, v in result.items():
        print(f"{k}: {v}")
    print("\n% missing by key field:")
    print((df[key_cols].isna().mean() * 100).round(1).to_string())
    return result

if __name__ == "__main__":
    op = pd.read_csv("data/open_payments_ky.csv", dtype=str)
    op_key_cols = [
        "covered_recipient_npi",
        "covered_recipient_specialty_1",
        "recipient_city",
        "recipient_zip_code",
        "applicable_manufacturer_or_applicable_gpo_making_payment_name",
        "total_amount_of_payment_usdollars",
        "date_of_payment",
        "product_category_or_therapeutic_area_1",
        "name_of_drug_or_biological_or_device_or_medical_supply_1",
    ]
    op_result = profile(op, "Open Payments", op_key_cols, ["record_id"],
                        "covered_recipient_npi", "date_of_payment")
    pd.DataFrame([op_result]).to_csv("output/profile_open_payments.csv", index=False)

    mc = pd.read_csv("data/medicare_ky.csv", dtype=str)
    mc_key_cols = [
        "Rndrng_NPI",
        "Rndrng_Prvdr_Last_Org_Name",
        "Rndrng_Prvdr_Type",
        "Rndrng_Prvdr_City",
        "Rndrng_Prvdr_Zip5",
        "Tot_Benes",
        "Tot_Srvcs",
        "Tot_Mdcr_Pymt_Amt",
        "Bene_Avg_Age",
    ]
    mc_result = profile(mc, "Medicare Providers", mc_key_cols, ["Rndrng_NPI"],
                        "Rndrng_NPI")
    pd.DataFrame([mc_result]).to_csv("output/profile_medicare.csv", index=False)

    npi = pd.read_csv("data/npi_registry_ky.csv", dtype=str)
    npi_found = npi[npi["found"] == "True"]
    npi_key_cols = [
        "npi",
        "enumeration_type",
        "status",
        "last_name",
        "credential",
        "primary_taxonomy",
        "practice_city",
        "practice_state",
        "practice_zip",
        "last_updated",
    ]
    npi_result = profile(npi_found, "NPI Registry", npi_key_cols, ["npi"],
                        "npi", "last_updated")
    npi_result["pct_npis_found"] = round(len(npi_found) / len(npi) * 100, 1)
    print(f"pct_npis_found: {npi_result['pct_npis_found']}")
    pd.DataFrame([npi_result]).to_csv("output/profile_npi.csv", index=False)