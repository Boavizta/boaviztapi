import pandas as pd
from pathlib import Path

AWS_PRICES = {
    "OnDemand": "On Demand",
    "LinuxReservedCost": "Linux Reserved cost",
    "LinuxSpotMinimumCost": "Linux Spot Minimum cost",
    "WindowsOnDemand": "Windows On Demand cost",
    "WindowsReservedCost": "Windows Reserved cost"
}

AZURE_PRICES = {
    "LinuxOnDemand": "Linux On Demand cost",
    "LinuxSavingsPlan": "Linux Savings Plan",
    "LinuxReservedCost": "Linux Reserved cost",
    "LinuxSpotCost": "Linux Spot cost",
    "WindowsOnDemand": "Windows On Demand cost",
    "WindowsSavingsPlan": "Windows Savings Plan",
    "WindowsReservedCost": "Windows Reserved cost",
    "WindowsSpotCost": "Windows Spot cost"
}

GCP_PRICES = {
    "LinuxOnDemand": "Linux On Demand cost",
    "LinuxSpotCost": "Linux Spot cost",
    "WindowsOnDemand": "Windows On Demand cost",
    "WindowsSpotCost": "Windows Spot cost"
}

def get_vantage_price(cloud_provider, instance_type, instancePricingType, region):
    base_path = Path(__file__).resolve().parent.parent / "data" / "vantage_prices"

    provider = cloud_provider.upper()
    if provider == "AWS":
        df = pd.read_csv(base_path / "aws_eu_frankfurt_1y_no_upfront.csv")
        price_map = AWS_PRICES
    elif provider == "AZURE":
        df = pd.read_csv(base_path / "azure_euw_1y_no_hybrid.csv")
        price_map = AZURE_PRICES
    elif provider == "GCP":
        df = pd.read_csv(base_path / "gcp_frankfurt.csv")
        price_map = GCP_PRICES
    else:
        raise ValueError("Unknown cloud provider")

    row = df[df["API Name"] == instance_type]
    if row.empty:
        raise ValueError(f"Instance {instance_type} not found in {provider} CSV")

    if instancePricingType not in price_map:
        raise ValueError(f"Pricing type '{instancePricingType}' not valid for {provider}")

    price_col = price_map[instancePricingType]
    price_str = row.iloc[0][price_col]

    if str(price_str).lower() == "unavailable":
        raise ValueError(f"Price for {instance_type} in {price_col} is unavailable")

    # Convert price string to float
    price = float(str(price_str).replace("€", "").replace(" hourly", "").replace(",", "."))
    return price
