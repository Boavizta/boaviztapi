#!/usr/bin/env python3
"""Check that cross-file references in the BoaviztAPI data files resolve.

Several CSV files refer to entries defined in another file: `server.csv` names a
CPU and a GPU that must exist in the crowdsourcing spec files, cloud instances
name the server platform they run on, regions name a provider and an electrical
mix, and so on. Nothing enforces those links at load time -- a typo silently
degrades into a bad fuzzy match or a fallback to defaults -- so this script
walks every reference and reports the ones that do not line up.

The name-based checks reuse the API's own fuzzy matchers, so what is reported
here is what the API would actually resolve at runtime.

Findings come in two levels:

  ERROR    the reference cannot be resolved at all (exact lookup missing, or no
           fuzzy candidate above the configured threshold)
  WARNING  the reference resolves, but not on an exact match: stray whitespace,
           a case difference, or a fuzzy hit on a different name

Usage (needs the project dependencies, so run it through poetry):
    poetry run python3 check_references.py            # full report
    poetry run python3 check_references.py --strict   # warnings also fail the run
    poetry run python3 check_references.py --quiet    # errors only
    poetry run python3 check_references.py --unused   # also list unreferenced platforms
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

# Make `boaviztapi` importable when the script is run directly from its folder.
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from boaviztapi import config  # noqa: E402
from boaviztapi.models.consumption_profile.consumption_profile import (  # noqa: E402
    CPUConsumptionProfileModel,
)
from boaviztapi.utils.fuzzymatch import (  # noqa: E402
    fuzzymatch_attr_from_cpu_name,
    fuzzymatch_attr_from_gpu_name,
    fuzzymatch_attr_from_pdf,
)

DATA_DIR = REPO_ROOT / "boaviztapi" / "data"
ARCHETYPES_DIR = DATA_DIR / "archetypes"
COMPONENTS_DIR = ARCHETYPES_DIR / "components"
CLOUD_DIR = ARCHETYPES_DIR / "cloud"
CROWDSOURCING_DIR = DATA_DIR / "crowdsourcing"
CONSUMPTION_PROFILE_DIR = DATA_DIR / "consumption_profile"

SERVER_CSV = ARCHETYPES_DIR / "server.csv"
CPU_SPECS_CSV = CROWDSOURCING_DIR / "cpu_specs.csv"
GPU_SPECS_CSV = CROWDSOURCING_DIR / "gpu_specs.csv"
ELECTRICAL_MIX_CSV = CROWDSOURCING_DIR / "electrical_mix.csv"
CPU_PROFILE_CSV = CONSUMPTION_PROFILE_DIR / "cpu" / "cpu_profile.csv"
PROVIDERS_CSV = CLOUD_DIR / "providers.csv"
REGIONS_CSV = CLOUD_DIR / "regions.csv"

ERROR = "ERROR"
WARNING = "WARNING"

# The DEFAULT rows of the component archetypes are the built-in fallbacks: they
# carry their own values and are not meant to point at a crowdsourcing entry.
DEFAULT_ARCHETYPE_ID = "DEFAULT"


class Report:
    """Collects findings, grouped by the check that produced them."""

    def __init__(self):
        self.findings = defaultdict(list)

    def add(self, check, level, location, message):
        self.findings[check].append((level, location, message))

    def error(self, check, location, message):
        self.add(check, ERROR, location, message)

    def warning(self, check, location, message):
        self.add(check, WARNING, location, message)

    def count(self, level):
        return sum(
            1 for items in self.findings.values() for lvl, _, _ in items if lvl == level
        )

    def print(self, quiet=False):
        for check, items in self.findings.items():
            shown = [i for i in items if not (quiet and i[0] == WARNING)]
            if not shown:
                continue
            print(f"\n## {check}")
            for level, location, message in shown:
                print(f"  {level:<7} {location}: {message}")


def read_rows(path):
    """Rows of a CSV as dicts, paired with their line number in the file."""
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Line 1 is the header, so the first data row is line 2.
        return [(lineno, row) for lineno, row in enumerate(reader, start=2)]


def cell(row, column):
    """Raw value of a column, tolerating a missing column."""
    value = row.get(column)
    return "" if value is None else value


def default_value(value):
    """First element of a `default;min;max` triplet, as stored in archetypes."""
    return value.split(";")[0].strip()


def as_float(value):
    try:
        return float(default_value(value))
    except (TypeError, ValueError):
        return None


def best_score(name, series):
    """Score the API's fuzzy matcher would give this name, for reporting."""
    lowered = name.lower()
    return series.str.lower().apply(lambda x: fuzz.token_set_ratio(x, lowered)).max()


def check_name_reference(report, check, location, raw_name, names, resolver, series):
    """Resolve one name against a spec file the way the API does at runtime.

    `names` is the set of known names, `resolver` the API's fuzzy matcher and
    `series` the column it scores against.
    """
    name = raw_name.strip()
    if name in names:
        if name != raw_name:
            report.warning(
                check, location, f"'{raw_name}' has leading/trailing whitespace"
            )
        return

    lowered = {n.lower(): n for n in names}
    if name.lower() in lowered:
        report.warning(
            check,
            location,
            f"'{raw_name}' differs by case from '{lowered[name.lower()]}'",
        )
        return

    match = resolver(name)
    if match is None:
        report.error(check, location, f"'{raw_name}' matches no entry")
        return

    report.warning(
        check,
        location,
        f"'{raw_name}' has no exact entry, fuzzy-matches "
        f"'{match[0]}' (score {best_score(name, series):.0f})",
    )


def check_cpu_names(report, cpu_specs):
    """server.csv and components/cpu.csv CPU names against cpu_specs.csv."""
    check = "CPU names -> crowdsourcing/cpu_specs.csv"
    names = set(cpu_specs["name"].dropna())
    series = cpu_specs["name"]

    def resolver(name):
        return fuzzymatch_attr_from_cpu_name(name, cpu_specs)

    for path, column, units_column in (
        (SERVER_CSV, "CPU.name", "CPU.units"),
        (COMPONENTS_DIR / "cpu.csv", "name", "units"),
    ):
        for lineno, row in read_rows(path):
            if row["id"].strip() == DEFAULT_ARCHETYPE_ID:
                continue
            location = f"{path.name}:{lineno} ({row['id']})"
            raw_name = cell(row, column)
            if not raw_name.strip():
                units = as_float(cell(row, units_column))
                if units:
                    report.warning(
                        check,
                        location,
                        f"{units_column}={units:g} but {column} is empty "
                        "(falls back to the default CPU)",
                    )
                continue
            check_name_reference(
                report, check, location, raw_name, names, resolver, series
            )


def check_cpu_families(report, cpu_specs):
    """components/cpu.csv `family` against the cpu_specs.csv code names."""
    check = "CPU families -> crowdsourcing/cpu_specs.csv (code_name)"
    path = COMPONENTS_DIR / "cpu.csv"
    code_names = set(cpu_specs["code_name"].dropna())

    for lineno, row in read_rows(path):
        if row["id"].strip() == DEFAULT_ARCHETYPE_ID:
            continue
        raw_family = cell(row, "family")
        family = raw_family.strip()
        if not family:
            continue
        location = f"{path.name}:{lineno} ({row['id']})"
        if family in code_names:
            continue
        match = fuzzymatch_attr_from_pdf(family, "code_name", cpu_specs)
        if match is None:
            report.error(check, location, f"'{raw_family}' matches no code_name")
        else:
            report.warning(
                check,
                location,
                f"'{raw_family}' has no exact code_name, fuzzy-matches '{match}'",
            )


def check_gpu_names(report, gpu_specs):
    """server.csv and components/gpu.csv GPU names against gpu_specs.csv."""
    check = "GPU names -> crowdsourcing/gpu_specs.csv"
    names = set(gpu_specs["name"].dropna())
    series = gpu_specs["name"]

    def resolver(name):
        return fuzzymatch_attr_from_gpu_name(name, gpu_specs)

    for path, column, units_column in (
        (SERVER_CSV, "GPU.name", "GPU.units"),
        (COMPONENTS_DIR / "gpu.csv", "name", None),
    ):
        for lineno, row in read_rows(path):
            if row["id"].strip() == DEFAULT_ARCHETYPE_ID:
                continue
            location = f"{path.name}:{lineno} ({row['id']})"
            raw_name = cell(row, column)
            units = as_float(cell(row, units_column)) if units_column else None
            if not raw_name.strip():
                if units:
                    report.warning(
                        check,
                        location,
                        f"{units_column}={units:g} but {column} is empty "
                        "(falls back to the default GPU)",
                    )
                continue
            if units_column and (units is None or units <= 0):
                raw_units = cell(row, units_column).strip() or "empty"
                report.error(
                    check,
                    location,
                    f"{column}='{raw_name.strip()}' but {units_column}="
                    f"{raw_units}; DeviceServer.gpu drops the GPU entirely "
                    "unless units is greater than 0, so the named GPU "
                    "contributes no impact",
                )
            check_name_reference(
                report, check, location, raw_name, names, resolver, series
            )


def check_case_types(report):
    """server.csv `CASE.case_type` against the case types in components/case.csv."""
    check = "Case types -> archetypes/components/case.csv"
    case_path = COMPONENTS_DIR / "case.csv"
    case_types = {
        cell(row, "case_type").strip().strip('"') for _, row in read_rows(case_path)
    }

    for lineno, row in read_rows(SERVER_CSV):
        raw_type = cell(row, "CASE.case_type")
        case_type = default_value(raw_type)
        if not case_type:
            continue
        if case_type not in case_types:
            report.error(
                f"{check}",
                f"{SERVER_CSV.name}:{lineno} ({row['id']})",
                f"case type '{raw_type}' is not one of {sorted(case_types)}",
            )


def cloud_provider_files():
    """Provider CSVs under archetypes/cloud, excluding the shared reference files."""
    excluded = {PROVIDERS_CSV.name, REGIONS_CSV.name}
    return sorted(p for p in CLOUD_DIR.glob("*.csv") if p.name not in excluded)


def check_cloud_platforms(report, server_ids):
    """Cloud instance `platform` against the server.csv ids (an exact lookup)."""
    check = "Cloud platforms -> archetypes/server.csv"
    for path in cloud_provider_files():
        for lineno, row in read_rows(path):
            raw_platform = cell(row, "platform")
            platform = raw_platform.strip()
            location = f"{path.name}:{lineno} ({row['id']})"
            if not platform:
                report.error(check, location, "no platform set")
                continue
            if platform in server_ids:
                if platform != raw_platform:
                    report.warning(
                        check,
                        location,
                        f"'{raw_platform}' has leading/trailing whitespace",
                    )
                continue
            # get_server_archetype does an exact id lookup, so anything else fails.
            report.error(
                check, location, f"platform '{raw_platform}' is not in server.csv"
            )


def check_providers(report):
    """Provider CSV names and regions.csv providers against providers.csv."""
    check = "Cloud providers -> archetypes/cloud/providers.csv"
    providers = {
        cell(row, "provider.name").strip() for _, row in read_rows(PROVIDERS_CSV)
    }

    for path in cloud_provider_files():
        if path.stem not in providers:
            report.error(
                check, path.name, f"'{path.stem}' is not declared in providers.csv"
            )

    declared_files = {p.stem for p in cloud_provider_files()}
    for provider in sorted(providers - declared_files):
        report.error(
            check, PROVIDERS_CSV.name, f"'{provider}' has no {provider}.csv file"
        )

    for lineno, row in read_rows(REGIONS_CSV):
        provider = cell(row, "provider").strip()
        if provider not in providers:
            report.error(
                check,
                f"{REGIONS_CSV.name}:{lineno}",
                f"provider '{provider}' is not in providers.csv",
            )


def check_regions(report):
    """regions.csv `usage_location` against the electrical mix country codes."""
    check = "Region usage locations -> crowdsourcing/electrical_mix.csv"
    with open(ELECTRICAL_MIX_CSV, encoding="utf-8") as f:
        header = next(csv.reader(f))
    # The first columns describe the impact factor, the rest are country codes.
    countries = set(header[7:])

    for lineno, row in read_rows(REGIONS_CSV):
        location_code = cell(row, "usage_location").strip()
        if not location_code:
            report.error(
                check,
                f"{REGIONS_CSV.name}:{lineno}",
                f"region '{cell(row, 'region')}' has no usage_location",
            )
        elif location_code not in countries:
            report.error(
                check,
                f"{REGIONS_CSV.name}:{lineno}",
                f"usage_location '{location_code}' is not a column of "
                "electrical_mix.csv",
            )


def check_consumption_profiles(report, cpu_specs):
    """CPUs used by servers against the consumption profile they resolve to.

    A CPU whose manufacturer and model range match no profile silently falls
    back to the generic one, so this is a warning rather than an error.
    """
    check = "CPU consumption profiles -> consumption_profile/cpu/cpu_profile.csv"
    reported = set()

    for lineno, row in read_rows(SERVER_CSV):
        name = cell(row, "CPU.name").strip()
        if not name:
            continue
        match = fuzzymatch_attr_from_cpu_name(name, cpu_specs)
        if match is None:
            continue  # already reported by check_cpu_names
        _, manufacturer, _, model_range = match[:4]
        key = (manufacturer, model_range)
        if key in reported:
            continue
        reported.add(key)

        if manufacturer is None or model_range is None:
            report.warning(
                check,
                f"{SERVER_CSV.name}:{lineno} ({row['id']})",
                f"'{name}' resolves to a cpu_specs entry with no "
                f"manufacturer/model_range (got {manufacturer!r}/{model_range!r})",
            )
            continue

        # Same lookup the API performs when building the consumption profile.
        profile = CPUConsumptionProfileModel.lookup_consumption_profile(
            cpu_manufacturer=manufacturer, cpu_model_range=model_range
        )
        if profile is None:
            report.warning(
                check,
                f"{SERVER_CSV.name}:{lineno} ({row['id']})",
                f"'{name}' resolves to {manufacturer} / {model_range}, which has "
                "no consumption profile (the generic profile is used)",
            )


def check_duplicate_ids(report):
    """Duplicate ids, which make every reference to them ambiguous."""
    check = "Duplicate ids"
    paths = [SERVER_CSV, ARCHETYPES_DIR / "user_terminal.csv"]
    paths += sorted(COMPONENTS_DIR.glob("*.csv"))
    paths += cloud_provider_files()

    for path in paths:
        seen = defaultdict(list)
        for lineno, row in read_rows(path):
            seen[cell(row, "id").strip()].append(lineno)
        for id_value, linenos in seen.items():
            if len(linenos) > 1:
                report.error(
                    check,
                    path.name,
                    f"id '{id_value}' appears {len(linenos)} times "
                    f"(lines {', '.join(str(n) for n in linenos)})",
                )


def report_unused_platforms(server_ids):
    """Server archetypes that no cloud instance points at."""
    used = set()
    for path in cloud_provider_files():
        for _, row in read_rows(path):
            used.add(cell(row, "platform").strip())

    unused = sorted(server_ids - used)
    print(
        f"\n## Server archetypes not referenced by any cloud instance ({len(unused)})"
    )
    for server_id in unused:
        print(f"  {server_id}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero on warnings as well as errors",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="only print errors, not warnings"
    )
    parser.add_argument(
        "--unused",
        action="store_true",
        help="also list server archetypes no cloud instance references",
    )
    args = parser.parse_args()

    cpu_specs = pd.read_csv(CPU_SPECS_CSV)
    gpu_specs = pd.read_csv(GPU_SPECS_CSV)
    server_ids = {cell(row, "id").strip() for _, row in read_rows(SERVER_CSV)}

    report = Report()
    check_cpu_names(report, cpu_specs)
    check_cpu_families(report, cpu_specs)
    check_gpu_names(report, gpu_specs)
    check_case_types(report)
    check_cloud_platforms(report, server_ids)
    check_providers(report)
    check_regions(report)
    check_consumption_profiles(report, cpu_specs)
    check_duplicate_ids(report)

    print(
        "Checking data file references "
        f"(CPU threshold {config.cpu_name_fuzzymatch_threshold}, "
        f"GPU threshold {config.gpu_name_fuzzymatch_threshold})"
    )
    report.print(quiet=args.quiet)

    if args.unused:
        report_unused_platforms(server_ids)

    errors = report.count(ERROR)
    warnings = report.count(WARNING)
    print(f"\n{errors} error(s), {warnings} warning(s)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
