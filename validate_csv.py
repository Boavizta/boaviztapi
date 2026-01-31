import subprocess
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
CSV_FILES = (
    (CLOUD_DIR.joinpath("aws.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("azure.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("gcp.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("ovhcloud.csv"), CLOUD_FORMAT_SPEC),
    (CLOUD_DIR.joinpath("scaleway.csv"), CLOUD_FORMAT_SPEC),
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
