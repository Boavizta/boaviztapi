import csv
import subprocess
import sys
from collections import Counter
from pathlib import Path

# This is a stand-alone script to run our CSV validation
# See the chkcsv doc for more info: https://pythonhosted.org/chkcsv/

DATA_DIR = Path("./boaviztapi/data")
ARCHETYPES_DIR = DATA_DIR.joinpath("archetypes")
CLOUD_DIR = ARCHETYPES_DIR.joinpath("cloud")
CROWDSOURCING_DIR = DATA_DIR.joinpath("crowdsourcing")

# All cloud instances share the same format spec
CLOUD_FORMAT_SPEC = CLOUD_DIR.joinpath("cloud.fmt")

# List of CSV files to check, in a tuple with the format file to use for the check.
# If no format file provided, chkcsv will look for a file with the same name and a .fmt extension.
PROVIDER_CSV_FILES = (
    (CLOUD_DIR.joinpath("aws.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("azure.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("gcp.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("ovhcloud.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("scaleway.csv"), CLOUD_FORMAT_SPEC),
)


def check_duplicate_ids(csv_file):
    """
    Check for duplicate IDs (first column) in a CSV file.
    This is equivalent to: cat file.csv | cut -f1 -d ',' | sort | uniq -c | sort -nr | grep -v '1 '
    Returns a dict with duplicated IDs and their counts, or empty dict if no duplicates.
    """
    ids = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Skip header
        next(reader, None)
        for row in reader:
            if row:  # Skip empty rows
                ids.append(row[0])

    id_counts = Counter(ids)
    # Return only duplicates (count > 1)
    duplicates = {id_val: count for id_val, count in id_counts.items() if count > 1}
    return duplicates


print("Checking for duplicate IDs in cloud CSV files...")

has_duplicates = False
for csv_path, _ in PROVIDER_CSV_FILES:
    duplicates = check_duplicate_ids(csv_path)
    if duplicates:
        has_duplicates = True
        print(f"\Duplicates in {csv_path.name}:")

if has_duplicates:
    print("ERROR: Duplicate IDs found in cloud CSV files!")
    sys.exit(1)

print("Validating CSV format with chkcsv...")

CSV_FILES = PROVIDER_CSV_FILES + (
    (ARCHETYPES_DIR.joinpath("server.csv"), None),
    (CROWDSOURCING_DIR.joinpath("cpu_specs.csv"), None),
)

for csv_file, format_spec in CSV_FILES:
    try:
        cmd = ["chkcsv.py", csv_file, "--columnexit"]
        if format_spec is not None:
            cmd.extend(["--formatspec", CLOUD_FORMAT_SPEC])

        subprocess.check_output(cmd)
        print(f"CSV {csv_file} valid")

    except subprocess.CalledProcessError as e:
        print(f"CSV {csv_file} falied validation")
        raise e
