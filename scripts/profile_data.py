import pandas as pd

def profile(df, source, key_cols, id_cols, npi_col, date_col):
    result = {"source": source, "rows": len(df), "columns": df.shape[1]}
    result["pct_missing_key_fields"] = round(df[key_cols].isna().mean().mean() * 100, 1)
    result["duplicate_rows"] = int(df.duplicated(subset=id_cols).sum())
    result["pct_rows_with_npi"] = round(df[npi_col].notna().mean() * 100, 1)
    result["unique_npis"] = int(df[npi_col].nunique())
    dates = pd.to_datetime(df[date_col], errors="coerce")
    result["earliest_date"] = dates.min().date()
    result["latest_date"] = dates.max().date()

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