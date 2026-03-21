# Scripts

Utilities for maintaining AWS EC2 instance data in BoaviztAPI. Both scripts use the AWS CLI (`aws ec2 describe-instance-types`) as their data source and require valid AWS credentials.

## compare_aws_instances.py

Compares the instance types currently in `boaviztapi/data/archetypes/cloud/aws.csv` against what the AWS API returns. Useful for auditing coverage before making changes.

Reports:
- Instance types present in AWS but missing from BoaviztAPI
- Instance types in BoaviztAPI that no longer exist in AWS
- Spec mismatches (vCPU, memory, storage, GPUs) for instances present in both

```sh
python scripts/compare_aws_instances.py
python scripts/compare_aws_instances.py --region eu-west-1
python scripts/compare_aws_instances.py --output report.csv
```

## update_aws_instances.py

Adds or updates instance entries in `aws.csv` and creates platform entries in `server.csv` for a given instance family or specific instance type. This is the Python replacement for the Go-based `addData.go` workflow in `boaviztapi/data/utils/complete_AWS_EC2/`.

```sh
# Add/update all instances in a family
python scripts/update_aws_instances.py c7g

# Add/update specific instance types
python scripts/update_aws_instances.py c7g.xlarge c7g.2xlarge

# Multiple families at once
python scripts/update_aws_instances.py c7g m7g r7g

# Preview changes without writing files
python scripts/update_aws_instances.py --dry-run c7g
```

New platform entries in `server.csv` require manual review: the AWS API does not expose the CPU model name, so `CPU.name` must be filled in by hand. `RAM.units` and `RAM.capacity` are estimated and should also be verified.

## Prerequisites

- Python 3.8+
- AWS CLI installed and configured (`aws configure`)
