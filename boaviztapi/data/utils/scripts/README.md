# Scripts

Utilities for maintaining the BoaviztAPI data files.

`check_references.py` works offline on the CSV files in `boaviztapi/data`. The two
AWS scripts use the AWS CLI (`aws ec2 describe-instance-types`) as their data
source and require valid AWS credentials. `compare_azure_instances.py` uses the
Azure CLI (`az vm list-skus`) and requires an Azure login.

## check_references.py

Checks that the cross-file references in the data files resolve. Nothing enforces
these links at load time, so a typo silently degrades into a bad fuzzy match or a
fallback to a default value.

What it checks:

- `CPU.name` in `server.csv` and `components/cpu.csv` against `crowdsourcing/cpu_specs.csv`
- `family` in `components/cpu.csv` against the `code_name` column of `cpu_specs.csv`
- `GPU.name` in `server.csv` and `components/gpu.csv` against `crowdsourcing/gpu_specs.csv`
- `GPU.units` in `server.csv` is above 0 wherever `GPU.name` is set
- `CASE.case_type` in `server.csv` against the case types in `components/case.csv`
- `platform` in each cloud provider CSV against the ids in `server.csv`
- provider CSV files against `cloud/providers.csv`, both ways, and the providers named in `cloud/regions.csv`
- `usage_location` in `cloud/regions.csv` against the country columns of `crowdsourcing/electrical_mix.csv`
- the consumption profile each server CPU resolves to, in `consumption_profile/cpu/cpu_profile.csv`
- duplicate ids in the archetype, component and cloud CSVs

The name-based checks call the API's own fuzzy matchers, so what is reported is
what the API would actually resolve at runtime. Findings come at two levels:
`ERROR` when a reference resolves to nothing, and `WARNING` when it only resolves
inexactly -- stray whitespace, a case difference, or a fuzzy hit on a different
name. The script exits non-zero when there is at least one error.

It imports `boaviztapi` itself to reuse the API's fuzzy matchers, so it needs the
project dependencies and has to run inside the poetry environment:

```sh
poetry run python3 check_references.py            # full report
poetry run python3 check_references.py --quiet    # errors only
poetry run python3 check_references.py --strict   # warnings fail the run too
poetry run python3 check_references.py --unused   # also list unreferenced server platforms
```

`poetry run` works from any directory inside the checkout. Note that poetry keys
its virtualenv to the project directory, so a git worktree needs its own
`poetry install`.

## compare_aws_instances.py

Compares the instance types currently in `boaviztapi/data/archetypes/cloud/aws.csv` against what the AWS API returns. Useful for auditing coverage before making changes.

Reports:
- Instance types present in AWS but missing from BoaviztAPI
- Instance types in BoaviztAPI that no longer exist in AWS
- Spec mismatches (vCPU, memory, storage, GPUs) for instances present in both

Instance types found only in BoaviztAPI are counted but not listed by default;
pass `--BoaviztaOnly` to list them (and include them in the CSV report).

```sh
python3 compare_aws_instances.py
python3 compare_aws_instances.py --region eu-west-1
python3 compare_aws_instances.py --output report.csv
python3 compare_aws_instances.py --BoaviztaOnly
```

## compare_azure_instances.py

Compares the VM sizes in `boaviztapi/data/archetypes/cloud/azure.csv` against the
Azure Resource SKUs API (`az vm list-skus`). It is the Azure counterpart of
`compare_aws_instances.py`.

Reports:
- VM sizes present in Azure but missing from BoaviztAPI, grouped by series, with
  their retirement date when Azure has announced one
- VM sizes in BoaviztAPI that Azure does not return
- Spec mismatches (vCPU, memory, storage, GPUs) for sizes present in both
- Sizes recorded in `azure.csv` under both `x` and `standard_x` whose specs differ

`az vm list-skus` takes a couple of minutes and returns one entry per size and
location (over 200 MB of JSON). The script condenses it to one record per size
and caches that in `~/.cache/boaviztapi/azure_vm_skus_<location|all>.json`.
Later runs read the cache and return in under a second. The cache is
refreshed when it is older than `--max-age-days` (7 by default), or on demand
with `--refresh`.

```sh
python3 compare_azure_instances.py
python3 compare_azure_instances.py --refresh
python3 compare_azure_instances.py --location westeurope
python3 compare_azure_instances.py --output report.csv
python3 compare_azure_instances.py --BoaviztaOnly
python3 compare_azure_instances.py --include-variants
```

Notes on the mapping:
- Azure names sizes `Standard_D2ads_v5`; both sides are lowercased and stripped
  of the `standard_` prefix before matching.
- `ssd_storage` is compared with the temporary disk (`MaxResourceVolumeMB`) plus
  any local NVMe (`NvmeDiskSizeInMiB`). The temporary disk is kept in GiB, as
  Azure quotes it. The NVMe is converted to decimal GB, as the drives are
  labelled. The comparison has a 5% tolerance (`--storage-tolerance`).
- Azure reports `GPUs=1` for sizes that get a partition of a GPU (NVv4,
  NVadsA10_v5), so a fractional `gpu_units` is accepted against 1.
- Constrained-vCPU sizes (`E4-2ds_v5`) and `_Promo` sizes are not listed as
  missing unless `--include-variants` is passed.
- The API does not expose the CPU model, so `platform` cannot be checked.

## update_aws_instances.py

Adds or updates instance entries in `aws.csv` and creates platform entries in `server.csv` for a given instance family or specific instance type. This is the Python replacement for the Go-based `addData.go` workflow in `boaviztapi/data/utils/complete_AWS_EC2/`.

```sh
# Add/update all instances in a family
python3 update_aws_instances.py c7g

# Add/update specific instance types
python3 update_aws_instances.py c7g.xlarge c7g.2xlarge

# Multiple families at once
python3 update_aws_instances.py c7g m7g r7g

# Preview changes without writing files
python3 update_aws_instances.py --dry-run c7g
```

New platform entries in `server.csv` require manual review: the AWS API does not expose the CPU model name, so `CPU.name` must be filled in by hand. `RAM.units` and `RAM.capacity` are estimated and should also be verified.

## Prerequisites

- Python 3.11+ (as required by `pyproject.toml`)
- For `check_references.py`: the project dependencies (`poetry install`), and the
  script invoked as `poetry run python3 check_references.py`
- For the two AWS scripts: the AWS CLI, installed and configured (`aws configure`).
  They do not import `boaviztapi`, so plain `python3` is enough.
- For `compare_azure_instances.py`: the Azure CLI, logged in (`az login`). It does
  not import `boaviztapi` either.
