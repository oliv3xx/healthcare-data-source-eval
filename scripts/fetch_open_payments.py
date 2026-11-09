import requests
import pandas as pd

BASE = "https://openpaymentsdata.cms.gov/api/1"

def find_dataset_id(title):
    resp = requests.get(f"{BASE}/metastore/schemas/dataset/items", timeout=60)
    resp.raise_for_status()
    for ds in resp.json():
        if ds.get("title") == title:
            return ds["identifier"]
    raise ValueError(f"Dataset not found: {title}")

def fetch_payments(dataset_id, state, max_rows=5000, page_size=500):
    rows = []
    offset = 0
    while len(rows) < max_rows:
        params = {
            "conditions[0][property]": "recipient_state",
            "conditions[0][value]": state,
            "conditions[0][operator]": "=",
            "conditions[1][property]": "indicate_drug_or_biological_or_device_or_medical_supply_1",
            "conditions[1][value]": "Device",
            "conditions[1][operator]": "=",
            "limit": page_size,
            "offset": offset,
        }
        resp = requests.get(f"{BASE}/datastore/query/{dataset_id}/0", params=params, timeout=120)
        resp.raise_for_status()
        batch = resp.json()["results"]
        if not batch:
            break
        rows.extend(batch)
        offset += page_size
        print(f"Fetched {len(rows)} rows")
    return pd.DataFrame(rows)

if __name__ == "__main__":
    ds_id = find_dataset_id("2024 General Payment Data")
    print("Dataset ID:", ds_id)
    df = fetch_payments(ds_id, "KY")
    df.to_csv("data/open_payments_ky.csv", index=False)
    print(df.shape)
    print(df.columns.tolist())