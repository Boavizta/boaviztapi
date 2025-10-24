import pandas as pd
import pycountry as pc

elecmaps = pd.read_csv('data/electricity/electricitymaps_zones.csv')
entsoe = pd.read_csv('data/electricity/eic_codes.csv')

## Join the two dataframes on the column "Country" and "country_name"
merged = pd.merge(elecmaps, entsoe, left_on="Country", right_on="country_name", how="left")

# Drop useless columns
merged.drop(columns=["country_name", "Day-ahead price", "Tier"], inplace=True)


def fuzzy_search_country_by_alpha2(alpha2):
    """Fuzzy search for country by alpha-2 code or name."""
    try:
        if "-" in alpha2:
            alpha2 = alpha2.split("-")[0].strip()
        return pc.countries.search_fuzzy(alpha2)[0].alpha_3
    except:
        return None


def fuzzy_search_country_by_name(country_name):
    """Fuzzy search for country by name."""
    try:
        return pc.countries.search_fuzzy(country_name)[0].alpha_3
    except:
        return None


# First, try to map by alpha-2 code
merged['alpha_3'] = merged["Zone Code"].map(fuzzy_search_country_by_alpha2)

# Then try to map by country name for missing values
if merged["alpha_3"].isnull().sum() > 0:
    missing = merged[merged["alpha_3"].isnull()]["Country"].unique()
    for country_name in missing:
        alpha_3 = fuzzy_search_country_by_name(country_name)
        merged.loc[merged["Country"] == country_name, "alpha_3"] = alpha_3

# Rename columns to python snakecase
merged.rename(columns={
    "Zone Code": "zone_code",
    "Zone name": "subdivision_name",
    "Country": "name",
    "EIC Code": "eic_code",
}, inplace=True)

# Fill NaN values with empty string to avoid issues with Pydantic and float conversions
merged.fillna(value='', inplace=True)
merged.to_csv('data/electricity/electricity_zones.csv', index=False)