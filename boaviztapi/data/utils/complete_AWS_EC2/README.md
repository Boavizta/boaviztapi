# Completing and updating AWS VMs data

## Source data

 1. Go to https://instances.vantage.sh.
 2. Add all columns
 3. Click export in upper right corner, left to the search bar.
 4. Override vantage-export.csv

## Workflow

The `addData.go` script reads `vantage-export.csv`, `aws.csv` and `cpu_specs.csv`. If an instance vantage-export.csv is not found in aws.csv, this instance is added.

For each instance family, if a **.metal** instance size exists, it is supposed that the main characteristics (CPU, RAM) of this instance matches the configuration of the hardware "platform" (here a platform means our best bet on the underlying hardware).

If not, the largest instance size of the family is used as the underlying platform.

In both cases, the platform identifier is added as a value of the platform column in `aws.csv`.

Hardware configuration of each platform is described in `archetypes/server.csv`.

Regarding storage, only the instances that have an explicit default storage volume in AWS documentation, with an explicit storage size, will get a storage value in aws.csv.

The storage of each platform, in server.csv, is the storage of the largest instance for the related family.

At this point, BoaviztAPI computes the impacts based on server.csv and aws.csv, using the [following methodology](https://doc.api.boavizta.org/Explanations/services/cloud/).
