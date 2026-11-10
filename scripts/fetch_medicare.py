import requests
import pandas as pd

# "latest" year of Medicare Physician & Other Practitioners - by Provider
URL = "https://data.cms.gov/data-api/v1/dataset/8889d81e-2ee7-448f-8713-f071038289b5/data"

def fetch_medicare(state, page_size=5000):
    rows = []
    offset = 0
    while True:
        params = {
            "filter[Rndrng_Prvdr_State_Abrvtn]": state,
            "size": page_size,
            "offset": offset,
        }
        resp = requests.get(URL, params=params, timeout=120)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        rows.extend(batch)
        offset += page_size
        print(f"Fetched {len(rows)} rows")
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = fetch_medicare("KY")
    df.to_csv("data/medicare_ky.csv", index=False)
    print(df.shape)
    print(df.columns.tolist())