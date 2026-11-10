import time
import requests
import pandas as pd

URL = "https://npiregistry.cms.hhs.gov/api/"

def lookup_npi(npi):
    params = {"version": "2.1", "number": npi}
    resp = requests.get(URL, params=params, timeout=30)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        return {"npi": npi, "found": False}
    r = results[0]
    basic = r.get("basic", {})
    primary_tax = next((t for t in r.get("taxonomies", []) if t.get("primary")), {})
    location = next((a for a in r.get("addresses", []) if a.get("address_purpose") == "LOCATION"), {})
    return {
        "npi": npi,
        "found": True,
        "enumeration_type": r.get("enumeration_type"),
        "status": basic.get("status"),
        "last_name": basic.get("last_name") or basic.get("organization_name"),
        "credential": basic.get("credential"),
        "primary_taxonomy": primary_tax.get("desc"),
        "practice_city": location.get("city"),
        "practice_state": location.get("state"),
        "practice_zip": location.get("postal_code"),
        "last_updated": basic.get("last_updated"),
    }

if __name__ == "__main__":
    op = pd.read_csv("data/open_payments_ky.csv", dtype=str)
    npis = op["covered_recipient_npi"].dropna().unique()
    rows = []
    for i, npi in enumerate(npis, start=1):
        try:
            rows.append(lookup_npi(npi))
        except requests.RequestException:
            rows.append({"npi": npi, "found": None})
        if i % 100 == 0:
            print(f"Looked up {i} of {len(npis)}")
        time.sleep(0.2)
    df = pd.DataFrame(rows)
    df.to_csv("data/npi_registry_ky.csv", index=False)
    print(df.shape)
    print(df["found"].value_counts(dropna=False))