import os

import numpy as np
import pandas as pd

from boaviztapi import data_dir

_electricity_emission_factors_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/electrical_mix.csv'))

def electical_mix_jsonify(electrical_mix):
    json = {"min-max": {}}
    for country_code in electrical_mix.columns:
        if country_code == "english_name" or country_code == "french_name" or country_code == "unit" or country_code == "source" or country_code == "priority" or country_code == "reference_year" or country_code == "name":
            continue
        if country_code not in json:
            json[country_code] = {}
            json[country_code]['country'] = electrical_mix[country_code][0]
        for index, row in electrical_mix.iterrows():
            if row["name"] == "renewable_energy" or row["name"] == "country":
                continue
            if np.isnan(float(row[country_code])):
                continue
            if row["name"] in json[country_code]:
                if row["priority"] > json[country_code][row["name"]]["priority"]:
                    continue

            json[country_code][row["name"]] = {}
            json[country_code][row["name"]]["unit"] = row["unit"]
            json[country_code][row["name"]]["source"] = row["source"]
            json[country_code][row["name"]]["priority"] = row["priority"]
            json[country_code][row["name"]]["reference_year"] = row["reference_year"]
            json[country_code][row["name"]]["value"] = float(row[country_code])

            if row["name"] not in json["min-max"]:
                json["min-max"][row["name"]] = {}
                json["min-max"][row["name"]]["min"] = float(row[country_code])
                json["min-max"][row["name"]]["max"] = float(row[country_code])
            else:
                if float(row[country_code]) < json["min-max"][row["name"]]["min"]:
                    json["min-max"][row["name"]]["min"] = float(row[country_code])
                if float(row[country_code]) > json["min-max"][row["name"]]["max"]:
                    json["min-max"][row["name"]]["max"] = float(row[country_code])

    return {"electricity": json}

if __name__ == '__main__':
    print(electical_mix_jsonify(_electricity_emission_factors_df))