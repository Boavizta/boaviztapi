#!/usr/bin/env python3
"""
Compare Azure VM sizes from the Azure Resource SKUs API with those in BoaviztAPI.

Requires:
  - Azure CLI logged in (`az login`) with access to a subscription
  - Python 3.8+

`az vm list-skus` is slow (well over a minute for all locations) and returns one
entry per size and location, so its output is condensed to one record per VM
size and cached locally. Subsequent runs reuse the cache until it is older than
--max-age-days or --refresh is passed.

Usage:
  python scripts/compare_azure_instances.py [--location westeurope] [--output report.csv]
                                            [--refresh] [--BoaviztaOnly] [--include-variants]
"""

import argparse
import csv
import json
import math
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BOAVIZTA_AZURE_CSV = (
    Path(__file__).resolve().parent.parent.parent / "archetypes" / "cloud" / "azure.csv"
)

CACHE_DIR = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "boaviztapi"
)
# Bump when the condensed record layout changes, to invalidate older caches.
CACHE_FORMAT = 2

# Splits a normalised size name into prefix, vCPU count, constrained-vCPU part
# and suffix, e.g. "e4-2ds_v5" -> ("e", "4", "-2", "ds_v5").
SIZE_RE = re.compile(r"^([a-z]+)(\d+)(-\d+)?(.*)$")


def fmt_num(value) -> str:
    """Render a number without a trailing .0 for whole values (0.125 stays 0.125)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def normalise(size_name: str) -> str:
    """Map an Azure size name or a BoaviztAPI id to a common key.

    The API names sizes "Standard_D2ads_v5"; azure.csv holds "d2ads_v5" and,
    for some sizes, also "standard_d2ads_v5".
    """
    name = size_name.lower()
    return name[len("standard_") :] if name.startswith("standard_") else name


def series(key: str) -> str:
    """Series of a normalised size name: "d2ads_v5" -> "dads_v5"."""
    m = SIZE_RE.match(key)
    return m.group(1) + m.group(4) if m else key


def load_boavizta_instances(csv_path: Path) -> dict:
    """Load VM sizes from BoaviztAPI azure.csv, keyed by their original id."""
    instances = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            instances[row["id"]] = {
                "vcpu": float(row["vcpu"]),
                "memory": float(row["memory"]),
                "ssd_storage": float(row.get("ssd_storage", 0) or 0),
                "hdd_storage": float(row.get("hdd_storage", 0) or 0),
                # Partitioned GPUs (NVv4) hold values like 0.125
                "gpu_units": float(row.get("gpu_units", 0) or 0),
                "platform": row.get("platform", ""),
            }
    return instances


def condense_skus(raw: list) -> dict:
    """Collapse the per-location SKU entries into one record per VM size.

    The capabilities of a size are the same in every location; only the
    location and its subscription restrictions differ.
    """
    sizes = {}
    for sku in raw:
        name = sku["name"]
        caps = {c["name"]: c["value"] for c in sku.get("capabilities") or []}
        restricted = set()
        for r in sku.get("restrictions") or []:
            if r.get("type") == "Location":
                restricted.update(r.get("values") or [])

        entry = sizes.get(name)
        if entry is None:
            entry = sizes[name] = {
                "vcpu": int(caps.get("vCPUs", 0)),
                "memory": float(caps.get("MemoryGB", 0)),
                # Temporary (resource) disk, in MiB
                "temp_disk_mib": int(caps.get("MaxResourceVolumeMB", 0) or 0),
                # Local NVMe disks (v6 sizes, L-series, HPC/GPU sizes), in MiB
                "nvme_disk_mib": int(caps.get("NvmeDiskSizeInMiB", 0) or 0),
                "gpus": float(caps.get("GPUs", 0) or 0),
                "arch": caps.get("CpuArchitectureType", ""),
                "vcpus_per_core": int(caps.get("vCPUsPerCore", 1) or 1),
                "parent_size": caps.get("ParentSize", ""),
                # MM/DD/YYYY; 01/01/9999 means no retirement is scheduled
                "retirement_date": caps.get("RetirementDateUtc", "").replace(
                    "01/01/9999", ""
                ),
                "azure_family": sku.get("family", ""),
                "locations": [],
                "available_locations": [],
            }
        for loc in sku.get("locations") or []:
            entry["locations"].append(loc)
            if loc not in restricted:
                entry["available_locations"].append(loc)

    for entry in sizes.values():
        entry["locations"].sort()
        entry["available_locations"].sort()
    return sizes


def fetch_azure_skus(location: str = None) -> dict:
    """Fetch VM sizes with `az vm list-skus` and condense them."""
    cmd = [
        "az",
        "vm",
        "list-skus",
        "--resource-type",
        "virtualMachines",
        # Include sizes not available to the current subscription
        "--all",
        "--output",
        "json",
    ]
    if location:
        cmd.extend(["--location", location])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return condense_skus(json.loads(result.stdout))


def cache_path(location: str = None) -> Path:
    return CACHE_DIR / f"azure_vm_skus_{location or 'all'}.json"


def load_azure_sizes(
    location: str, cache_file: Path, refresh: bool, max_age_days: float
) -> dict:
    """Return the condensed Azure sizes, from the cache when it is fresh enough."""
    if not refresh and cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text())
        except (OSError, json.JSONDecodeError):
            cached = None
        if cached and cached.get("format") == CACHE_FORMAT:
            age_days = (time.time() - cached["fetched_at"]) / 86400
            if age_days <= max_age_days:
                fetched = datetime.fromtimestamp(cached["fetched_at"], timezone.utc)
                print(
                    f"Using cached Azure SKUs from {cache_file} "
                    f"(fetched {fetched:%Y-%m-%d %H:%M} UTC, {age_days:.1f} days old; "
                    "pass --refresh to fetch again)"
                )
                return cached["sizes"]
            print(f"Cache {cache_file} is {age_days:.1f} days old, refreshing")

    where = f"location {location}" if location else "all locations"
    print(f"Fetching Azure VM SKUs for {where} (this can take a few minutes)...")
    sizes = fetch_azure_skus(location)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(
        json.dumps(
            {
                "format": CACHE_FORMAT,
                "fetched_at": time.time(),
                "location": location,
                "sizes": sizes,
            }
        )
    )
    print(f"  Cached to {cache_file}")
    return sizes


def azure_specs(entry: dict) -> dict:
    """Azure capabilities expressed in the units used by azure.csv."""
    return {
        "vcpu": float(entry["vcpu"]),
        "memory": entry["memory"],
        # azure.csv records the temporary disk plus any local NVMe, in GiB
        "ssd_storage": (entry["temp_disk_mib"] + entry["nvme_disk_mib"]) / 1024,
        "hdd_storage": 0.0,
        "gpu_units": entry["gpus"],
    }


def diff_specs(b: dict, a: dict, storage_tolerance: float) -> dict:
    """Spec differences between a BoaviztAPI row and the Azure specs."""
    diffs = {}
    if b["vcpu"] != a["vcpu"]:
        diffs["vcpu"] = (b["vcpu"], a["vcpu"])
    if abs(b["memory"] - a["memory"]) > 0.01 * max(a["memory"], 1):
        diffs["memory"] = (b["memory"], a["memory"])
    if abs(b["ssd_storage"] - a["ssd_storage"]) > storage_tolerance * max(
        a["ssd_storage"], 1
    ):
        diffs["ssd_storage"] = (b["ssd_storage"], a["ssd_storage"])
    if b["hdd_storage"] != a["hdd_storage"]:
        diffs["hdd_storage"] = (b["hdd_storage"], a["hdd_storage"])
    # Azure reports GPUs=1 for sizes that get a partition of a GPU (NVv4,
    # NVadsA10_v5), so a fraction in azure.csv is accepted against 1.
    partitioned = a["gpu_units"] == 1 and 0 < b["gpu_units"] < 1
    if not partitioned and not math.isclose(
        b["gpu_units"], a["gpu_units"], abs_tol=1e-9
    ):
        diffs["gpu_units"] = (b["gpu_units"], a["gpu_units"])
    return diffs


def compare(
    boavizta: dict, azure: dict, include_variants: bool, storage_tolerance: float
) -> dict:
    """Compare BoaviztAPI and Azure VM size sets."""
    azure_by_key = {normalise(name): name for name in azure}

    boavizta_keys = {}
    for iid in boavizta:
        boavizta_keys.setdefault(normalise(iid), []).append(iid)

    # Constrained-vCPU sizes (E4-2ds_v5) and promo sizes are variants of a
    # regular size; they are only listed as missing with --include-variants.
    def is_variant(name: str) -> bool:
        return bool(azure[name]["parent_size"]) or name.lower().endswith("_promo")

    only_azure = []
    skipped_variants = 0
    for key, name in azure_by_key.items():
        if key in boavizta_keys:
            continue
        if is_variant(name) and not include_variants:
            skipped_variants += 1
            continue
        only_azure.append(name)

    only_boavizta = sorted(
        iid
        for key, ids in boavizta_keys.items()
        if key not in azure_by_key
        for iid in ids
    )

    mismatches = []
    common = 0
    for key, ids in sorted(boavizta_keys.items()):
        if key not in azure_by_key:
            continue
        common += 1
        name = azure_by_key[key]
        a = azure_specs(azure[name])
        for iid in ids:
            diffs = diff_specs(boavizta[iid], a, storage_tolerance)
            if diffs:
                mismatches.append({"id": iid, "azure_name": name, "diffs": diffs})

    # Sizes recorded under both "x" and "standard_x" whose specs disagree. The
    # platform can legitimately differ (e.g. Dasv4-Type1 vs Dasv4-Type2 hosts).
    def specs(iid):
        return {k: v for k, v in boavizta[iid].items() if k != "platform"}

    inconsistent_aliases = []
    for key, ids in sorted(boavizta_keys.items()):
        if len(ids) > 1:
            if any(specs(i) != specs(ids[0]) for i in ids[1:]):
                inconsistent_aliases.append(ids)

    return {
        "only_in_azure": sorted(only_azure, key=normalise),
        "only_in_boavizta": only_boavizta,
        "common_count": common,
        "alias_count": sum(1 for ids in boavizta_keys.values() if len(ids) > 1),
        "inconsistent_aliases": inconsistent_aliases,
        "skipped_variants": skipped_variants,
        "mismatches": mismatches,
    }


def retirement_note(entry: dict) -> str:
    date = entry.get("retirement_date", "")
    return f" (retiring {date})" if date else ""


def print_report(
    result: dict, azure: dict, boavizta_count: int, show_boavizta_only: bool = False
):
    """Print a human-readable report."""
    print("=" * 70)
    print("Azure VM sizes vs BoaviztAPI Instance Comparison Report")
    print("=" * 70)

    print(f"\nTotal in Azure API:    {len(azure)}")
    print(f"Total in BoaviztAPI:   {boavizta_count}")
    print(f"Common sizes:          {result['common_count']}")
    print(f"Only in Azure:         {len(result['only_in_azure'])}")
    if result["skipped_variants"]:
        print(
            f"  (plus {result['skipped_variants']} constrained-vCPU/promo variants, "
            "see --include-variants)"
        )
    print(f"Only in BoaviztAPI:    {len(result['only_in_boavizta'])}")
    print(f"With spec mismatches:  {len(result['mismatches'])}")
    print(
        f"Ids in both forms:     {result['alias_count']} "
        "(x and standard_x in azure.csv)"
    )

    if result["only_in_azure"]:
        print(f"\n--- Sizes only in Azure ({len(result['only_in_azure'])}) ---")
        groups = {}
        for name in result["only_in_azure"]:
            groups.setdefault(series(normalise(name)), []).append(name)
        for group in sorted(groups):
            names = groups[group]
            labels = [normalise(n) + retirement_note(azure[n]) for n in names]
            no_access = all(not azure[n]["available_locations"] for n in names)
            suffix = "  [not available to this subscription]" if no_access else ""
            print(f"  {group}: {', '.join(labels)}{suffix}")

    if result["only_in_boavizta"]:
        if show_boavizta_only:
            print(
                f"\n--- Sizes only in BoaviztAPI ({len(result['only_in_boavizta'])}) ---"
            )
            for iid in result["only_in_boavizta"]:
                print(f"  {iid}")
        else:
            print(
                f"\n(Use --BoaviztaOnly to list the {len(result['only_in_boavizta'])} "
                "sizes found only in BoaviztAPI)"
            )

    if result["inconsistent_aliases"]:
        print(
            f"\n--- Ids in both forms with different specs "
            f"({len(result['inconsistent_aliases'])}) ---"
        )
        for ids in result["inconsistent_aliases"]:
            print(f"  {', '.join(ids)}")

    if result["mismatches"]:
        print(f"\n--- Spec mismatches ({len(result['mismatches'])}) ---")
        for m in result["mismatches"]:
            entry = azure[m["azure_name"]]
            print(f"  {m['id']}:")
            for field, (b, a) in m["diffs"].items():
                detail = ""
                if field == "ssd_storage" and entry["nvme_disk_mib"]:
                    detail = (
                        f"  (temp {fmt_num(entry['temp_disk_mib'] / 1024)}"
                        f" + nvme {fmt_num(entry['nvme_disk_mib'] / 1024)} GiB)"
                    )
                print(f"    {field}: boavizta={fmt_num(b)}  azure={fmt_num(a)}{detail}")


def write_csv_report(
    result: dict, azure: dict, output_path: str, show_boavizta_only: bool = False
):
    """Write a detailed CSV report."""

    def size_columns(name):
        entry = azure[name]
        a = azure_specs(entry)
        return [
            fmt_num(a["vcpu"]),
            fmt_num(a["memory"]),
            fmt_num(entry["temp_disk_mib"] / 1024),
            fmt_num(entry["nvme_disk_mib"] / 1024),
            fmt_num(a["gpu_units"]),
            series(normalise(name)),
            entry["arch"],
            entry["retirement_date"],
        ]

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "status",
                "id",
                "vcpu",
                "memory_gib",
                "temp_disk_gib",
                "nvme_disk_gib",
                "gpu_units",
                "series",
                "architecture",
                "retirement_date",
                "diff_field",
                "boavizta_value",
                "azure_value",
            ]
        )
        for name in result["only_in_azure"]:
            writer.writerow(
                ["missing_from_boavizta", normalise(name)]
                + size_columns(name)
                + ["", "", ""]
            )
        if show_boavizta_only:
            for iid in result["only_in_boavizta"]:
                writer.writerow(["missing_from_azure", iid] + [""] * 11)
        for m in result["mismatches"]:
            for field, (b, a) in m["diffs"].items():
                writer.writerow(
                    ["mismatch", m["id"]]
                    + size_columns(m["azure_name"])
                    + [field, fmt_num(b), fmt_num(a)]
                )
    print(f"\nCSV report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare Azure VM sizes with BoaviztAPI data"
    )
    parser.add_argument(
        "--location",
        default=None,
        help="Azure location to query, e.g. westeurope (default: all locations)",
    )
    parser.add_argument("--output", default=None, help="Path for CSV output report")
    parser.add_argument(
        "--csv-path",
        default=str(BOAVIZTA_AZURE_CSV),
        help="Path to BoaviztAPI azure.csv",
    )
    parser.add_argument(
        "--cache-file",
        default=None,
        help=f"Cache file for the Azure SKUs (default: {cache_path()})",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Ignore the cache and query the Azure API again",
    )
    parser.add_argument(
        "--max-age-days",
        type=float,
        default=7,
        help="Refetch when the cache is older than this (default: 7)",
    )
    parser.add_argument(
        "--storage-tolerance",
        type=float,
        default=0.05,
        help="Relative tolerance on ssd_storage (default: 0.05)",
    )
    parser.add_argument(
        "--include-variants",
        action="store_true",
        help="Also list constrained-vCPU and promo sizes missing from BoaviztAPI",
    )
    parser.add_argument(
        "--BoaviztaOnly",
        "--boavizta-only",
        dest="boavizta_only",
        action="store_true",
        help="List the sizes found only in BoaviztAPI (hidden by default)",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"Error: BoaviztAPI CSV not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading BoaviztAPI sizes from {csv_path}...")
    boavizta = load_boavizta_instances(csv_path)
    print(f"  Found {len(boavizta)} sizes")

    cache_file = Path(args.cache_file) if args.cache_file else cache_path(args.location)
    try:
        azure = load_azure_sizes(
            args.location, cache_file, args.refresh, args.max_age_days
        )
    except subprocess.CalledProcessError as e:
        print(f"Error calling Azure CLI: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Error: Azure CLI not found. See "
            "https://learn.microsoft.com/cli/azure/install-azure-cli",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"  Found {len(azure)} sizes")

    result = compare(boavizta, azure, args.include_variants, args.storage_tolerance)
    print_report(result, azure, len(boavizta), args.boavizta_only)

    if args.output:
        write_csv_report(result, azure, args.output, args.boavizta_only)


if __name__ == "__main__":
    main()
