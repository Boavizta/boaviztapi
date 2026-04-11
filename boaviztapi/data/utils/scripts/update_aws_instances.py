#!/usr/bin/env python3
"""
Fetch AWS EC2 instance type info and create/update entries in BoaviztAPI data files.

Updates:
  - boaviztapi/data/archetypes/cloud/aws.csv  (cloud instance definitions)
  - boaviztapi/data/archetypes/server.csv      (platform/server definitions)

Requires:
  - AWS CLI configured with valid credentials
  - Python 3.8+

Usage:
  # Update all instances in the c7g family
  python scripts/update_aws_instances.py c7g

  # Update specific instance types
  python scripts/update_aws_instances.py c7g.xlarge c7g.2xlarge

  # Update multiple families
  python scripts/update_aws_instances.py c7g m7g r7g

  # Dry-run mode (show what would change without writing)
  python scripts/update_aws_instances.py --dry-run c7g
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "archetypes"
AWS_CSV = DATA_DIR / "cloud" / "aws.csv"
SERVER_CSV = DATA_DIR / "server.csv"
CPU_SPECS_CSV = (
    Path(__file__).resolve().parent.parent.parent / "crowdsourcing" / "cpu_specs.csv"
)

AWS_CSV_FIELDS = [
    "id",
    "vcpu",
    "memory",
    "ssd_storage",
    "hdd_storage",
    "gpu_units",
    "platform",
    "source",
]

SERVER_CSV_FIELDS = [
    "id",
    "manufacturer",
    "CASE.case_type",
    "CPU.units",
    "CPU.core_units",
    "CPU.die_size_per_core",
    "CPU.name",
    "CPU.threads",
    "RAM.units",
    "RAM.capacity",
    "SSD.units",
    "SSD.capacity",
    "HDD.units",
    "HDD.capacity",
    "GPU.units",
    "GPU.name",
    "GPU.memory_capacity",
    "POWER_SUPPLY.units",
    "POWER_SUPPLY.unit_weight",
    "USAGE.time_workload",
    "USAGE.use_time_ratio",
    "USAGE.hours_life_time",
    "USAGE.other_consumption_ratio",
    "WARNINGS",
]

# Ported from addData.go: hardcoded map of family -> platform instance size.
# For families with a .metal instance, use "metal".
# For families without, use the largest available size.
# This is the authoritative mapping; new families default to "metal".
PLATFORM_SIZE = {
    "a1": "metal",
    "c1": "xlarge",
    "c3": "8xlarge",
    "c4": "8xlarge",
    "c5": "metal",
    "c5a": "24xlarge",
    "c5ad": "24xlarge",
    "c5d": "metal",
    "c5n": "metal",
    "c6a": "metal",
    "c6g": "metal",
    "c6gd": "metal",
    "c6gn": "16xlarge",
    "c6i": "metal",
    "c6id": "metal",
    "c6in": "metal",
    "c7a": "metal-48xl",
    "c7g": "metal",
    "c7gd": "16xlarge",
    "c7gn": "16xlarge",
    "c7i": "48xlarge",
    "c8g": "metal-24xl",
    "d3": "8xlarge",
    "d3en": "12xlarge",
    "f1": "16xlarge",
    "g2": "8xlarge",
    "g3": "16xlarge",
    "g4ad": "16xlarge",
    "g4dn": "metal",
    "g5": "48xlarge",
    "g5g": "metal",
    "g6": "48xlarge",
    "g6e": "48xlarge",
    "gr6": "48xlarge",
    "h1": "16xlarge",
    "hpc6a": "48xlarge",
    "hpc7a": "96xlarge",
    "hpc7g": "16xlarge",
    "hs1": "8xlarge",
    "i2": "8xlarge",
    "i3": "metal",
    "i3en": "metal",
    "i4g": "16xlarge",
    "i4i": "metal",
    "i8g": "metal-24xl",
    "im4gn": "16xlarge",
    "inf1": "24xlarge",
    "inf2": "48xlarge",
    "is4gen": "metal",
    "m1": "xlarge",
    "m2": "4xlarge",
    "m3": "2xlarge",
    "m4": "16xlarge",
    "m5": "metal",
    "m5a": "24xlarge",
    "m5ad": "24xlarge",
    "m5d": "metal",
    "m5dn": "metal",
    "m5n": "metal",
    "m5zn": "metal",
    "m6a": "metal",
    "m6g": "metal",
    "m6gd": "metal",
    "m6i": "metal",
    "m6id": "metal",
    "m6idn": "metal",
    "m6in": "metal",
    "m7a": "metal-48xl",
    "m7g": "metal",
    "m7gd": "metal",
    "m7i": "48xlarge",
    "m7i-flex": "8xlarge",
    "m8g": "metal-24xl",
    "mac1": "metal",
    "mac2": "metal",
    "mac2-m2pro": "metal",
    "p2": "16xlarge",
    "p3": "16xlarge",
    "p3dn": "24xlarge",
    "p4d": "24xlarge",
    "p4de": "24xlarge",
    "p5": "48xlarge",
    "r3": "8xlarge",
    "r4": "16xlarge",
    "r5": "metal",
    "r5a": "24xlarge",
    "r5ad": "24xlarge",
    "r5b": "metal",
    "r5d": "metal",
    "r5dn": "metal",
    "r5n": "metal",
    "r6a": "metal",
    "r6g": "metal",
    "r6gd": "metal",
    "r6i": "metal",
    "r6id": "metal",
    "r6idn": "metal",
    "r6in": "metal",
    "r7a": "metal-48xl",
    "r7g": "metal",
    "r7gd": "16xlarge",
    "r7i": "metal-48xl",
    "r7iz": "32xlarge",
    "r8g": "metal-24xl",
    "ra3": "16xlarge",
    "t1": "micro",
    "t2": "2xlarge",
    "t3": "2xlarge",
    "t3a": "2xlarge",
    "t4g": "2xlarge",
    "trn1": "32xlarge",
    "trn1n": "32xlarge",
    "u-3tb1": "56xlarge",
    "u-6tb1": "metal",
    "u-9tb1": "metal",
    "u-12tb1": "metal",
    "u-18tb1": "metal",
    "u-24tb1": "metal",
    "vt1": "24xlarge",
    "x1": "32xlarge",
    "x1e": "32xlarge",
    "x2gd": "metal",
    "x2idn": "metal",
    "x2iedn": "metal",
    "x2iezn": "metal",
    "x8g": "metal-24xl",
    "z1d": "metal",
}


def get_family(instance_type: str) -> str:
    """Extract family from instance type (e.g., 'c7g' from 'c7g.xlarge')."""
    if "." in instance_type:
        return instance_type.split(".")[0]
    return instance_type


def get_platform_id(family: str) -> str:
    """Get the platform instance id for a family.

    Uses the hardcoded PLATFORM_SIZE map (ported from addData.go).
    Falls back to {family}.metal for unknown families.
    """
    size = PLATFORM_SIZE.get(family, "metal")
    return f"{family}.{size}"


def load_csv(csv_path: Path) -> tuple[list[str], list[dict]]:
    """Load a CSV file, returning (fieldnames, rows as dicts)."""
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


def write_csv(csv_path: Path, fieldnames: list[str], rows: list[dict]):
    """Write rows back to a CSV file (unix line endings)."""
    import io

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    # csv module uses \r\n internally; normalize to \n
    text = buf.getvalue().replace("\r\n", "\n")
    csv_path.write_text(text, newline="")


def load_cpu_specs() -> dict:
    """Load cpu_specs.csv into a dict keyed by CPU name.

    Returns {name: {"tdp": str, "cores": str}} mirroring addData.go's usage.
    """
    specs = {}
    if not CPU_SPECS_CSV.exists():
        return specs
    with open(CPU_SPECS_CSV, newline="") as f:
        for row in csv.DictReader(f):
            specs[row["name"]] = {
                "tdp": row.get("tdp", ""),
                "cores": row.get("cores", ""),
            }
    return specs


# ---------------------------------------------------------------------------
# AWS API fetching (filtered by family or specific instance types)
# ---------------------------------------------------------------------------


def fetch_aws_instances(targets: list[str], region: str) -> dict:
    """Fetch instance types from AWS.

    targets: families ('c7g') or specific types ('c7g.xlarge').
    """
    families = []
    specific = []
    for t in targets:
        if "." in t:
            specific.append(t)
        else:
            families.append(t)

    result = {}
    if specific:
        result.update(_fetch(region, instance_types=specific))
    for fam in families:
        result.update(_fetch(region, family_filter=f"{fam}.*"))
    return result


def _fetch(
    region: str,
    instance_types: list[str] | None = None,
    family_filter: str | None = None,
) -> dict:
    """Call describe-instance-types with pagination."""
    instances = {}
    next_token = None

    while True:
        cmd = [
            "aws",
            "ec2",
            "describe-instance-types",
            "--region",
            region,
            "--output",
            "json",
        ]
        if instance_types:
            cmd.extend(["--instance-types"] + instance_types)
        if family_filter:
            cmd.extend(
                [
                    "--filters",
                    f"Name=instance-type,Values={family_filter}",
                ]
            )
        if next_token:
            cmd.extend(["--next-token", next_token])

        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)

        for it in data.get("InstanceTypes", []):
            instances[it["InstanceType"]] = _parse_instance(it)

        next_token = data.get("NextToken")
        if not next_token:
            break

    return instances


def _parse_instance(it: dict) -> dict:
    """Parse a single InstanceType entry from the AWS API."""
    # Storage
    ssd_gb = 0
    hdd_gb = 0
    ssd_disk_count = 0
    ssd_disk_size = 0
    hdd_disk_count = 0
    hdd_disk_size = 0
    storage_info = it.get("InstanceStorageInfo")
    if it.get("InstanceStorageSupported") and storage_info:
        for disk in storage_info.get("Disks", []):
            count = disk.get("Count", 1)
            size = disk.get("SizeInGB", 0)
            total = size * count
            if disk.get("Type") == "ssd":
                ssd_gb += total
                ssd_disk_count += count
                ssd_disk_size = size
            elif disk.get("Type") == "hdd":
                hdd_gb += total
                hdd_disk_count += count
                hdd_disk_size = size

    # GPU
    gpu_count = 0
    gpu_name = ""
    gpu_memory_per_unit = 0
    gpu_info = it.get("GpuInfo")
    if gpu_info and gpu_info.get("Gpus"):
        gpus = gpu_info["Gpus"]
        gpu_count = sum(g.get("Count", 0) for g in gpus)
        gpu_name = gpus[0].get("Name", "")
        total_mem_mib = gpus[0].get("MemoryInfo", {}).get("SizeInMiB", 0)
        if gpu_count > 0 and total_mem_mib > 0:
            gpu_memory_per_unit = total_mem_mib // 1024  # MiB -> GiB per unit

    proc = it.get("ProcessorInfo", {})

    return {
        "vcpu": it["VCpuInfo"]["DefaultVCpus"],
        "memory_gib": it["MemoryInfo"]["SizeInMiB"] / 1024,
        "ssd_storage": ssd_gb,
        "hdd_storage": hdd_gb,
        "gpu_units": gpu_count,
        "gpu_name": gpu_name,
        "gpu_memory_per_unit": gpu_memory_per_unit,
        "bare_metal": it.get("BareMetal", False),
        "arch": proc.get("SupportedArchitectures", []),
        "cpu_manufacturer": proc.get("Manufacturer", ""),
        # Per-disk info for server.csv platform entries
        "ssd_disk_count": ssd_disk_count,
        "ssd_disk_size": ssd_disk_size,
        "hdd_disk_count": hdd_disk_count,
        "hdd_disk_size": hdd_disk_size,
    }


# ---------------------------------------------------------------------------
# Platform (server.csv) logic — ported from addData.go
# ---------------------------------------------------------------------------


def estimate_cpu_units(platform_data: dict) -> int:
    """Estimate CPU socket count.

    Ported from addData.go getCPUUnits: Graviton/ARM = 1 socket,
    Intel/AMD typically 2 for large instances.
    """
    arch = platform_data.get("arch", [])
    mfr = platform_data.get("cpu_manufacturer", "")
    if "arm64" in arch or "Graviton" in mfr or "AWS" in mfr:
        return 1
    return 2


def estimate_ram(total_memory_gib: float) -> tuple[int, int]:
    """Estimate RAM units and per-DIMM capacity.

    Ported from addData.go getRAM: uses 32 GiB DIMMs as default,
    falls back to total memory for small instances.
    """
    if total_memory_gib < 32:
        return 1, int(total_memory_gib)
    capacity = 32
    units = int(total_memory_gib / capacity)
    return units, capacity


def build_server_row(
    platform_id: str,
    platform_data: dict,
    cpu_specs: dict,
) -> dict:
    """Build a server.csv row for a new platform.

    Mirrors the logic in addData.go for populating platform fields,
    with defaults matching existing entries in server.csv.
    """
    row = {field: "" for field in SERVER_CSV_FIELDS}
    row["id"] = platform_id
    row["manufacturer"] = "AWS"
    row["CASE.case_type"] = "rack"

    # CPU
    cpu_units = estimate_cpu_units(platform_data)
    row["CPU.units"] = str(cpu_units)
    # CPU.name cannot be reliably determined from the AWS API
    # (it only provides manufacturer, not model). Leave empty for
    # manual completion — the Go script got this from Vantage's
    # PhysicalProcessor field.
    row["CPU.name"] = ""
    row["CPU.core_units"] = ""
    row["CPU.die_size_per_core"] = ""
    row["CPU.threads"] = ""

    # RAM (ported from addData.go getRAM)
    ram_units, ram_capacity = estimate_ram(platform_data["memory_gib"])
    row["RAM.units"] = str(ram_units)
    row["RAM.capacity"] = str(ram_capacity)

    # Storage — use per-disk counts from the platform instance
    # (ported from addData.go: platform storage = largest instance storage)
    row["SSD.units"] = str(platform_data["ssd_disk_count"])
    row["SSD.capacity"] = str(platform_data["ssd_disk_size"])
    row["HDD.units"] = str(platform_data["hdd_disk_count"])
    row["HDD.capacity"] = str(platform_data["hdd_disk_size"])

    # GPU
    row["GPU.units"] = str(platform_data["gpu_units"])
    row["GPU.name"] = platform_data.get("gpu_name", "")
    row["GPU.memory_capacity"] = str(platform_data.get("gpu_memory_per_unit", 0))

    # Defaults matching existing AWS entries in server.csv
    row["POWER_SUPPLY.units"] = "2;2;2"
    row["POWER_SUPPLY.unit_weight"] = "2.99;1;5"
    row["USAGE.time_workload"] = "50;0;100"
    row["USAGE.use_time_ratio"] = "1"
    row["USAGE.hours_life_time"] = "52560"
    row["USAGE.other_consumption_ratio"] = "0.33;0.2;0.6"
    row["WARNINGS"] = "RAM configuration was not verified"

    return row


# ---------------------------------------------------------------------------
# aws.csv helpers
# ---------------------------------------------------------------------------


def format_number(value: float) -> str:
    """Format a number: int when whole, float otherwise."""
    if value == int(value):
        return str(int(value))
    return str(value)


def build_cloud_row(instance_id: str, data: dict, platform_id: str) -> dict:
    """Build an aws.csv row."""
    return {
        "id": instance_id,
        "vcpu": format_number(data["vcpu"]),
        "memory": format_number(data["memory_gib"]),
        "ssd_storage": format_number(data["ssd_storage"]),
        "hdd_storage": format_number(data["hdd_storage"]),
        "gpu_units": format_number(data["gpu_units"]),
        "platform": platform_id,
        "source": "",
    }


# ---------------------------------------------------------------------------
# Update logic
# ---------------------------------------------------------------------------


def resolve_platforms(
    aws_instances: dict,
    existing_cloud_rows: list[dict],
) -> dict[str, str]:
    """Resolve family -> platform_id mapping.

    1. If the family already has entries in aws.csv, reuse their platform.
    2. Otherwise, use PLATFORM_SIZE map (from addData.go).
    3. For completely unknown families, fall back to {family}.metal.
    """
    # Collect existing platform assignments per family
    existing = {}
    for row in existing_cloud_rows:
        fam = get_family(row["id"])
        if row.get("platform"):
            existing.setdefault(fam, row["platform"])

    families = {get_family(iid) for iid in aws_instances}
    mapping = {}
    for fam in sorted(families):
        if fam in existing:
            mapping[fam] = existing[fam]
        else:
            mapping[fam] = get_platform_id(fam)
    return mapping


def update_server_csv(
    aws_instances: dict,
    platform_map: dict[str, str],
    cpu_specs: dict,
    dry_run: bool,
) -> tuple[int, int]:
    """Create missing platform entries in server.csv.

    Does NOT overwrite existing entries (they may have been
    manually curated with correct CPU names, RAM configs, etc.).
    Returns (added, skipped).
    """
    fieldnames, rows = load_csv(SERVER_CSV)
    existing_ids = {row["id"] for row in rows}

    added = 0
    skipped = 0
    platform_ids = set(platform_map.values())

    for pid in sorted(platform_ids):
        if pid in existing_ids:
            print(f"  Platform already exists: {pid}")
            skipped += 1
            continue

        if pid not in aws_instances:
            print(
                f"  WARNING: platform {pid} not in fetched data "
                f"(not available in this region?)"
            )
            continue

        new_row = build_server_row(pid, aws_instances[pid], cpu_specs)
        rows.append(new_row)
        added += 1
        print(f"  Added platform: {pid}")
        print(
            f"    CPU.units={new_row['CPU.units']}, "
            f"RAM={new_row['RAM.units']}x{new_row['RAM.capacity']}GB"
        )
        if new_row["GPU.units"] != "0":
            print(
                f"    GPU={new_row['GPU.units']}x "
                f"{new_row['GPU.name']} "
                f"({new_row['GPU.memory_capacity']}GB each)"
            )
        print(
            "    ACTION REQUIRED: fill in CPU.name manually "
            "(AWS API does not expose processor model)"
        )

    if not dry_run and added:
        write_csv(SERVER_CSV, fieldnames, rows)
        print(f"\n  Wrote {SERVER_CSV}")

    return added, skipped


def update_aws_csv(
    aws_instances: dict,
    platform_map: dict[str, str],
    dry_run: bool,
) -> tuple[int, int]:
    """Add/update instance entries in aws.csv.

    Returns (added, updated).
    """
    fieldnames, rows = load_csv(AWS_CSV)
    row_index = {row["id"]: i for i, row in enumerate(rows)}

    added = 0
    updated = 0

    for iid in sorted(aws_instances.keys()):
        family = get_family(iid)
        platform_id = platform_map.get(family, "")
        new_row = build_cloud_row(iid, aws_instances[iid], platform_id)

        if iid in row_index:
            old_row = rows[row_index[iid]]
            # Preserve existing source URL and platform if we
            # don't have better data
            if old_row.get("source") and not new_row["source"]:
                new_row["source"] = old_row["source"]
            if old_row.get("platform") and not new_row["platform"]:
                new_row["platform"] = old_row["platform"]

            changes = {
                f: (old_row.get(f), new_row[f])
                for f in AWS_CSV_FIELDS
                if old_row.get(f) != new_row[f]
            }
            if changes:
                rows[row_index[iid]] = new_row
                updated += 1
                print(f"  Updated: {iid}")
                for field, (old, new) in changes.items():
                    print(f"    {field}: {old!r} -> {new!r}")
        else:
            rows.append(new_row)
            added += 1
            print(f"  Added: {iid}")

    if not dry_run and (added or updated):
        write_csv(AWS_CSV, fieldnames, rows)
        print(f"\n  Wrote {AWS_CSV}")

    return added, updated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch AWS EC2 instance types and update BoaviztAPI "
            "data files (aws.csv and server.csv). "
            "Accepts instance families (e.g. c7g) or specific "
            "types (e.g. c7g.xlarge)."
        ),
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help=("Instance families (e.g. c7g) or specific types (e.g. c7g.xlarge)"),
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region to query (default: us-east-1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no files will be modified ===\n")

    # Fetch from AWS
    print(f"Fetching from AWS ({args.region})...")
    try:
        aws_instances = fetch_aws_instances(args.targets, args.region)
    except subprocess.CalledProcessError as e:
        print(
            f"Error calling AWS CLI: {e.stderr}",
            file=sys.stderr,
        )
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Error: AWS CLI not found. Install it with: pip install awscli",
            file=sys.stderr,
        )
        sys.exit(1)

    if not aws_instances:
        print(
            "No matching instance types found.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"  Found {len(aws_instances)} instance types\n")

    # Load existing data
    _, existing_cloud_rows = load_csv(AWS_CSV)
    cpu_specs = load_cpu_specs()

    # Resolve platform mapping
    platform_map = resolve_platforms(aws_instances, existing_cloud_rows)
    print("Platform mapping:")
    for fam, pid in sorted(platform_map.items()):
        print(f"  {fam} -> {pid}")
    print()

    # Update server.csv first (platforms must exist before
    # aws.csv references them)
    print("--- server.csv (platforms) ---")
    srv_added, srv_skipped = update_server_csv(
        aws_instances, platform_map, cpu_specs, args.dry_run
    )
    if not srv_added and not srv_skipped:
        print("  No platforms to process")
    print()

    # Update aws.csv
    print("--- aws.csv (cloud instances) ---")
    cloud_added, cloud_updated = update_aws_csv(
        aws_instances, platform_map, args.dry_run
    )
    if not cloud_added and not cloud_updated:
        print("  No changes needed")
    print()

    # Summary
    print("=" * 50)
    print("Summary:")
    print(f"  aws.csv:    {cloud_added} added, {cloud_updated} updated")
    print(f"  server.csv: {srv_added} added, {srv_skipped} already existed")
    if args.dry_run:
        print("\n  (dry run — no files were modified)")
    if srv_added:
        print(
            "\n  NOTE: New platform entries need manual review:"
            "\n  - Fill in CPU.name (processor model)"
            "\n  - Verify RAM.units and RAM.capacity"
        )


if __name__ == "__main__":
    main()
