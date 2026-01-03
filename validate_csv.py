import subprocess
from pathlib import Path

# This is a stand-alone script to run our CSV validation
# See the chkcsv doc for more info
# https://pythonhosted.org/chkcsv/

DATA_DIR = Path("./boaviztapi/data")
ARCHETYPES_DIR = DATA_DIR.joinpath("archetypes")
CLOUD_DIR = ARCHETYPES_DIR.joinpath("cloud")
CROWDSOURCING_DIR = DATA_DIR.joinpath("crowdsourcing")

CSV_FILES = (
    CLOUD_DIR.joinpath("aws.csv"),
    CLOUD_DIR.joinpath("azure.csv"),
    CLOUD_DIR.joinpath("gcp.csv"),
    CLOUD_DIR.joinpath("scaleway.csv"),
    ARCHETYPES_DIR.joinpath("server.csv"),
    CROWDSOURCING_DIR.joinpath("cpu_specs.csv"),
)

for csv_file in CSV_FILES:
    try:
        subprocess.check_output(["chkcsv.py", csv_file, "--columnexit"])
        print(f"CSV {csv_file} valid")
    except subprocess.CalledProcessError as e:
        print(f"CSV {csv_file} falied validation")
        raise e
