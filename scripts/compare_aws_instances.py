#!/usr/bin/env python3
"""
Compare AWS EC2 instance types from the AWS API with those in BoaviztAPI.

Requires:
  - AWS CLI configured with valid credentials
  - Python 3.8+

Usage:
  python scripts/compare_aws_instances.py [--region us-east-1] [--output report.csv]
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

BOAVIZTA_AWS_CSV = Path(__file__).resolve().parent.parent / "boaviztapi" / "data" / "archetypes" / "cloud" / "aws.csv"


def load_boavizta_instances(csv_path: Path) -> dict:
    """Load instance types from BoaviztAPI aws.csv."""
    instances = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            instances[row["id"]] = {
                "vcpu": float(row["vcpu"]),
                "memory": float(row["memory"]),
                "ssd_storage": float(row.get("ssd_storage", 0) or 0),
                "hdd_storage": float(row.get("hdd_storage", 0) or 0),
                "gpu_units": int(row.get("gpu_units", 0) or 0),
                "platform": row.get("platform", ""),
            }
    return instances


def fetch_aws_instance_types(region: str) -> dict:
    """Fetch all instance types from AWS EC2 describe-instance-types (paginated)."""
    instances = {}
    next_token = None

    while True:
        cmd = [
            "aws", "ec2", "describe-instance-types",
            "--region", region,
            "--output", "json",
        ]
        if next_token:
            cmd.extend(["--next-token", next_token])

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        for it in data.get("InstanceTypes", []):
            instance_id = it["InstanceType"]

            # Compute total instance storage
            ssd_gb = 0
            hdd_gb = 0
            if it.get("InstanceStorageSupported") and it.get("InstanceStorageInfo"):
                for disk in it["InstanceStorageInfo"].get("Disks", []):
                    total = disk.get("SizeInGB", 0) * disk.get("Count", 1)
                    if disk.get("Type") == "ssd":
                        ssd_gb += total
                    elif disk.get("Type") == "hdd":
                        hdd_gb += total

            gpu_count = 0
            if it.get("GpuInfo") and it["GpuInfo"].get("Gpus"):
                gpu_count = sum(g.get("Count", 0) for g in it["GpuInfo"]["Gpus"])

            instances[instance_id] = {
                "vcpu": it["VCpuInfo"]["DefaultVCpus"],
                "memory": it["MemoryInfo"]["SizeInMiB"] / 1024,  # MiB -> GiB
                "ssd_storage": ssd_gb,
                "hdd_storage": hdd_gb,
                "gpu_units": gpu_count,
                "family": instance_id.split(".")[0] if "." in instance_id else instance_id,
                "arch": it["ProcessorInfo"].get("SupportedArchitectures", []),
                "hypervisor": it.get("Hypervisor", ""),
                "bare_metal": it.get("BareMetal", False),
            }

        next_token = data.get("NextToken")
        if not next_token:
            break

    return instances


def compare(boavizta: dict, aws: dict) -> dict:
    """Compare BoaviztAPI and AWS instance sets."""
    boavizta_ids = set(boavizta.keys())
    aws_ids = set(aws.keys())

    only_aws = sorted(aws_ids - boavizta_ids)
    only_boavizta = sorted(boavizta_ids - aws_ids)
    common = sorted(boavizta_ids & aws_ids)

    mismatches = []
    for iid in common:
        b = boavizta[iid]
        a = aws[iid]
        diffs = {}
        if b["vcpu"] != a["vcpu"]:
            diffs["vcpu"] = {"boavizta": b["vcpu"], "aws": a["vcpu"]}
        # Compare memory with 1% tolerance (GiB rounding)
        if abs(b["memory"] - a["memory"]) > 0.01 * max(a["memory"], 1):
            diffs["memory"] = {"boavizta": b["memory"], "aws": a["memory"]}
        if b["ssd_storage"] != a["ssd_storage"]:
            diffs["ssd_storage"] = {"boavizta": b["ssd_storage"], "aws": a["ssd_storage"]}
        if b["hdd_storage"] != a["hdd_storage"]:
            diffs["hdd_storage"] = {"boavizta": b["hdd_storage"], "aws": a["hdd_storage"]}
        if b["gpu_units"] != a["gpu_units"]:
            diffs["gpu_units"] = {"boavizta": b["gpu_units"], "aws": a["gpu_units"]}
        if diffs:
            mismatches.append({"id": iid, "diffs": diffs})

    return {
        "only_in_aws": only_aws,
        "only_in_boavizta": only_boavizta,
        "common_count": len(common),
        "mismatches": mismatches,
    }


def print_report(result: dict, aws: dict):
    """Print a human-readable report."""
    print("=" * 70)
    print("AWS EC2 vs BoaviztAPI Instance Comparison Report")
    print("=" * 70)

    print(f"\nTotal in AWS API:      {len(aws)}")
    print("Total in BoaviztAPI:   (see common + only_in_boavizta)")
    print(f"Common instances:      {result['common_count']}")
    print(f"Only in AWS:           {len(result['only_in_aws'])}")
    print(f"Only in BoaviztAPI:    {len(result['only_in_boavizta'])}")
    print(f"With spec mismatches:  {len(result['mismatches'])}")

    if result["only_in_aws"]:
        print(f"\n--- Instances only in AWS ({len(result['only_in_aws'])}) ---")
        # Group by family
        families = {}
        for iid in result["only_in_aws"]:
            family = iid.split(".")[0] if "." in iid else iid
            families.setdefault(family, []).append(iid)
        for family in sorted(families):
            instances = families[family]
            print(f"  {family}: {', '.join(instances)}")

    if result["only_in_boavizta"]:
        print(f"\n--- Instances only in BoaviztAPI ({len(result['only_in_boavizta'])}) ---")
        for iid in result["only_in_boavizta"]:
            print(f"  {iid}")

    if result["mismatches"]:
        print(f"\n--- Spec mismatches ({len(result['mismatches'])}) ---")
        for m in result["mismatches"]:
            print(f"  {m['id']}:")
            for field, vals in m["diffs"].items():
                print(f"    {field}: boavizta={vals['boavizta']}  aws={vals['aws']}")


def write_csv_report(result: dict, aws: dict, output_path: str):
    """Write detailed CSV report of missing instances."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "status", "id", "vcpu", "memory_gib", "ssd_storage_gb",
            "hdd_storage_gb", "gpu_units", "family", "architectures",
            "diff_field", "boavizta_value", "aws_value",
        ])
        for iid in result["only_in_aws"]:
            a = aws[iid]
            writer.writerow([
                "missing_from_boavizta", iid, a["vcpu"], a["memory"],
                a["ssd_storage"], a["hdd_storage"], a["gpu_units"],
                a["family"], ";".join(a["arch"]), "", "", "",
            ])
        for iid in result["only_in_boavizta"]:
            writer.writerow([
                "missing_from_aws", iid, "", "", "", "", "", "", "", "", "", "",
            ])
        for m in result["mismatches"]:
            for field, vals in m["diffs"].items():
                a = aws[m["id"]]
                writer.writerow([
                    "mismatch", m["id"], a["vcpu"], a["memory"],
                    a["ssd_storage"], a["hdd_storage"], a["gpu_units"],
                    a["family"], ";".join(a["arch"]),
                    field, vals["boavizta"], vals["aws"],
                ])
    print(f"\nCSV report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compare AWS EC2 instance types with BoaviztAPI data")
    parser.add_argument("--region", default="us-east-1", help="AWS region to query (default: us-east-1)")
    parser.add_argument("--output", default=None, help="Path for CSV output report")
    parser.add_argument("--csv-path", default=str(BOAVIZTA_AWS_CSV), help="Path to BoaviztAPI aws.csv")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"Error: BoaviztAPI CSV not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading BoaviztAPI instances from {csv_path}...")
    boavizta = load_boavizta_instances(csv_path)
    print(f"  Found {len(boavizta)} instances")

    print(f"Fetching AWS instance types from region {args.region}...")
    try:
        aws = fetch_aws_instance_types(args.region)
    except subprocess.CalledProcessError as e:
        print(f"Error calling AWS CLI: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: AWS CLI not found. Install it with: pip install awscli", file=sys.stderr)
        sys.exit(1)
    print(f"  Found {len(aws)} instances")

    result = compare(boavizta, aws)
    print_report(result, aws)

    if args.output:
        write_csv_report(result, aws, args.output)


if __name__ == "__main__":
    main()
