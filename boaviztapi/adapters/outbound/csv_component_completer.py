import os
from typing import Optional

import pandas as pd

from boaviztapi import data_dir
from boaviztapi.core.ports.component_completer import ComponentCompleter
from boaviztapi.utils.fuzzymatch import (
    fuzzymatch_attr_from_cpu_name,
    fuzzymatch_attr_from_pdf,
)

import boaviztapi.utils.fuzzymatch as _fuzzymatch_mod

# Ensure pandas Series has .fuzzymatch() for consumption profile lookups
_fuzzymatch_mod.pandas()

_cpu_specs = pd.read_csv(os.path.join(data_dir, "crowdsourcing/cpu_specs.csv"))
_ram_df = pd.read_csv(os.path.join(data_dir, "crowdsourcing/ram_manufacture.csv"))
_ssd_df = pd.read_csv(os.path.join(data_dir, "crowdsourcing/ssd_manufacture.csv"))
_cpu_profile_df = pd.read_csv(
    os.path.join(data_dir, "consumption_profile/cpu/cpu_profile.csv")
)


class CsvComponentCompleter(ComponentCompleter):
    """Adapter that completes component specs from CSV files and fuzzy matching."""

    def complete_cpu_from_name(self, cpu_name: str) -> Optional[dict]:
        result = fuzzymatch_attr_from_cpu_name(cpu_name, _cpu_specs)
        if result is None:
            return None
        (
            name,
            manufacturer,
            family,
            model_range,
            tdp,
            core_units,
            threads,
            die_size,
            die_size_source,
            source,
        ) = result
        return {
            "name": name,
            "manufacturer": manufacturer,
            "family": family,
            "model_range": model_range,
            "tdp": tdp,
            "core_units": core_units,
            "threads": threads,
            "die_size": die_size,
            "die_size_source": die_size_source,
            "source": source,
        }

    def complete_ram_density(
        self,
        manufacturer: Optional[str] = None,
        process: Optional[float] = None,
    ) -> Optional[dict]:
        sub = _ram_df

        corrected_manufacturer = None
        if manufacturer is not None:
            corrected = fuzzymatch_attr_from_pdf(manufacturer, "manufacturer", sub)
            if corrected is not None:
                sub = sub[sub["manufacturer"] == corrected]
                corrected_manufacturer = corrected

        if process is not None:
            sub = sub[sub["process"] == process]

        if len(sub) == 0 or (len(sub) == len(_ram_df)):
            return None

        if len(sub) == 1:
            return {
                "density": float(sub["density"].iloc[0]),
                "source": str(sub["manufacturer"].iloc[0]),
                "min": float(sub["density"].iloc[0]),
                "max": float(sub["density"].iloc[0]),
                "manufacturer": corrected_manufacturer,
            }

        return {
            "density": float(sub["density"].mean()),
            "source": "Average of " + str(len(sub)) + " rows",
            "min": float(sub["density"].min()),
            "max": float(sub["density"].max()),
            "manufacturer": corrected_manufacturer,
        }

    def complete_ssd_density(
        self,
        manufacturer: Optional[str] = None,
        layers: Optional[int] = None,
    ) -> Optional[dict]:
        sub = _ssd_df

        corrected_manufacturer = None
        if manufacturer is not None:
            corrected = fuzzymatch_attr_from_pdf(manufacturer, "manufacturer", sub)
            if corrected is not None:
                sub = sub[sub["manufacturer"] == corrected]
                corrected_manufacturer = corrected

        if layers is not None:
            sub = sub[sub["layers"] == layers]

        if len(sub) == 0 or (len(sub) == len(_ssd_df)):
            return None

        if len(sub) == 1:
            source = (
                str(sub["source"].iloc[0])
                if "source" in sub.columns
                else str(sub["manufacturer"].iloc[0])
            )
            return {
                "density": float(sub["density"].iloc[0]),
                "source": source,
                "min": float(sub["density"].iloc[0]),
                "max": float(sub["density"].iloc[0]),
                "manufacturer": corrected_manufacturer,
            }

        return {
            "density": float(sub["density"].mean()),
            "source": "Average of " + str(len(sub)) + " rows",
            "min": float(sub["density"].min()),
            "max": float(sub["density"].max()),
            "manufacturer": corrected_manufacturer,
        }

    def get_cpu_consumption_profile(
        self,
        cpu_manufacturer: Optional[str] = None,
        cpu_model_range: Optional[str] = None,
    ) -> Optional[dict]:
        sub = _cpu_profile_df

        if cpu_manufacturer is not None:
            tmp = sub[sub["manufacturer"].fuzzymatch(cpu_manufacturer)]
            if len(tmp) > 0:
                sub = tmp.copy()

        if cpu_model_range is not None:
            tmp = sub[sub["model_range"].fuzzymatch(cpu_model_range)]
            if len(tmp) > 0:
                sub = tmp.copy()

        if len(sub) == 1:
            row = sub.iloc[0]
            return {k: row[k] for k in ["a", "b", "c", "d"]}
        elif len(sub) > 1:
            if cpu_model_range is not None:
                exact_match = sub[
                    sub["model_range"].str.lower() == cpu_model_range.lower()
                ]
                if len(exact_match) > 0:
                    row = exact_match.iloc[0]
                    return {k: row[k] for k in ["a", "b", "c", "d"]}
        return None
