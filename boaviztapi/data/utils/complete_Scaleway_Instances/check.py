import requests

CLOUD_URL="http://localhost:5000/v1/cloud/instance"
PROVIDERS_URL=f"{CLOUD_URL}/all_providers"
VALID_INSTANCE_TYPE="dev1-l"

def main():
    resp = requests.get(PROVIDERS_URL)

    if not resp.ok:
        print(f"Providers request failed: {resp.json()}")
        exit(1)

    if "scaleway" in resp.json():
        print("Found Scaleway in list of providers")
    else:
        print("Did not find Scaleway in list of providers: {resp.status_code}")
        exit(1)

    url_params = {
        "provider": "scaleway",
        "instance_type": VALID_INSTANCE_TYPE,
        "verbose": True,
        "duration": "100",
        }

    resp = requests.get(CLOUD_URL, params=url_params)
    if resp.ok:
        print(f"Got response to impact request for type {VALID_INSTANCE_TYPE}")
    else:
        print("Did not find Scaleway in list of providers: {resp.status_code}")
        exit(1)

    resp_body = resp.json()
    for impact_name, impact in resp_body["impacts"].items():
        print(f"\nGot {impact_name}: {impact}")

    cpu = resp_body["verbose"]["CPU-1"]["model_range"]["value"]
    print(f"\nGot CPU model: {cpu}")

if __name__ == "__main__":
    main()
