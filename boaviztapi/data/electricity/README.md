# Electricity Data Integration

This document describes the process of merging data from Electricity Maps and ENTSO-E (European Network of Transmission
System Operators for Electricity) datasets.

## Dataset Overview

### Electricity Maps Zones (electricitymaps_zones.csv)

- Contains geographical zones and their corresponding codes used by Electricity Maps API
- Provides carbon intensity and power generation data for different regions
- Maps country codes to specific electricity market zones

### ENTSO-E EIC Codes (eic_codes.csv)

- Contains Energy Identification Codes (EIC) used by ENTSO-E
- Maps countries to their respective electricity market areas
- Includes pricing information for different market zones

## Data Integration Process

The datasets are automatically merged using the `merge_electricity_zones.py` script, which:

1. Reads both CSV files (electricitymaps_zones.csv and eic_codes.csv)
2. Creates a unified mapping between different identifier systems
3. Maintains a consistent reference system for accessing data from both sources

To update the merged dataset, simply run the merge_electricity_zones.py script:
