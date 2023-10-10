import os

import numpy as np
import pandas as pd

from boaviztapi import data_dir
from boaviztapi.model.impact import IMPACT_CRITERIAS

_electricity_emission_factors_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/electrical_mix.csv'))
_iot_impact_factors_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/iot_factors_tide.csv'), header=1)


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


def iot_jsonify(df):
    json = {"IoT": {}}
    df[['functional_block', 'hsl_level']] = df['api_name'].str.split(' - ', expand=True)
    df.index.names = ['api_name']
    for functional_block in df['functional_block'].unique():
        if functional_block == "Name" or functional_block == "api_name" or functional_block == "Unit":
            continue
        json["IoT"][functional_block] = {}
        for hsl_level in df[df["functional_block"] == functional_block]['hsl_level'].unique():
            if hsl_level is None:
                continue
            json["IoT"][functional_block][hsl_level] = {}
            json["IoT"][functional_block][hsl_level]["manufacture"] = {}
            json["IoT"][functional_block][hsl_level]["eol"] = {}
            json["IoT"][functional_block][hsl_level]["source"] = "Adapted by Tide from 'Assessing the embodied carbon footprint of IoT edge devices with a bottom-up life-cycle approach', 2021; Thibault Pirson et David Bol (Université catholique de Louvain, ICTEAM/ECS, Louvain-la-Neuve, Belgique)"

            for impact in IMPACT_CRITERIAS:
                if df[(df["functional_block"] == functional_block) & (df["hsl_level"] == hsl_level)].get(f"eol-{impact.name}") is None:
                    continue
                json["IoT"][functional_block][hsl_level]["manufacture"][impact.name] = float(df[(df["functional_block"] == functional_block) & (df["hsl_level"] == hsl_level)].get(f"fab-{impact.name}").iloc[0])
                json["IoT"][functional_block][hsl_level]["eol"][impact.name] = float(df[(df["functional_block"] == functional_block) & (df["hsl_level"] == hsl_level)].get(f"eol-{impact.name}").iloc[0])

    return json

if __name__ == '__main__':
    print(iot_jsonify(_iot_impact_factors_df))
