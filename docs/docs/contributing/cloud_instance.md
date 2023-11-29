# Add a new cloud instance

This guide will you add a new cloud instances for a cloud provider that is already supported by BoaviztAPI.

## Cloud instances CSV file

All instances for one particular cloud provider are stored in a CSV file named after that cloud provider (e.g. `aws.csv` for AWS). These files are located at `boaviztapi/data/archetypes/cloud/`.

| Column name                   | Required     | Description                                                         | Example                   | 
|-------------------------------|--------------|---------------------------------------------------------------------|---------------------------|
| id                            | **Required** | Instance identifier                                                 | c5.2xlarge                |
| manufacturer                  | **Required** | Cloud provider                                                      | AWS                       |
| CASE.type                     |              | Type of enclosure (usually "rack")                                  | rack                      |
| year                          |              | ???                                                                 | 2016                      |
| vcpu                          | **Required** | Number of vCPU                                                      | 8                         |
| platform_vcpu                 | **Required** | Number of vCPU of the platform[^1]                                  | 96                        |
| CPU.units                     |              | Number of physical CPU                                              | 2                         |
| CPU.name                      |              | CPU name[^2]                                                        | Xeon Platinum 8124M       |
| CPU.core_units                |              | Number of CPU cores per CPU                                         | 24                        |
| CPU.manufacturer              |              | CPU manufacturer                                                    | Intel                     |
| CPU.model_range               |              | CPU model range                                                     | Xeon Platinum             |
| CPU.family                    |              | CPU family                                                          | Skylake                   |
| CPU.tdp                       |              | CPU TDP (in Watt)                                                   | 240                       |
| CPU.manufacture_date          |              | CPU manufacture date                                                | 2016                      |
| instance.ram_capacity         | **Required** | Instance RAM capacity (in GB)                                       | 16                        |
| RAM.units                     |              | Number of RAM banks                                                 | 12                        |
| RAM.capacity                  |              | RAM bank capacity                                                   | 16                        |
| SSD.units                     |              | Number of SSD disks                                                 | 1                         |
| SSD.capacity                  |              | Capacity of SSD disk (in GB)                                        | 512                       |
| HDD.units                     |              | Number of HDD disks                                                 | 1                         |
| HDD.capacity                  |              | Capacity of HDD disk (in GB)                                        | 4096                      |
| GPU.units                     |              | Number of GPU cards                                                 | 4                         |
| GPU.name                      |              | GPU name                                                            | NVIDIA A10G               |
| GPU.tdp                       |              | GPU TDP value (in Watt)                                             | 150                       |
| GPU.memory_capacity           |              | GPU memory capacity (in GB)                                         | 24                        |
| POWER_SUPPLY.units            |              | Number of power supplies                                            | 2                         |
| POWER_SUPPLY.unit_weight      |              | Power supply weight (in kg)                                         | 2.99;1;5                  |
| USAGE.instance_per_server     |              | Number of instances hosted by the same platform                     | 12                        |
| USAGE.time_workload           |              | Percentage of workload                                              | 50;0;100                  |
| USAGE.hours_life_time         |              | Number of hours of life time                                        | 35040 _(=4 years)_        |
| USAGE.use_time_ratio          |              | Proportion of the time the instance is being used                   | 0.5                       |
| USAGE.other_consumption_ratio |              | Power consumption ratio of other components relative to RAM and CPU | 0.33;0.2;0.6              |
| USAGE.overcommited            |              | ???                                                                 | 0                         |
| Warnings                      |              | List of warnings separated by semi-colons (;)                       | RAM.capacity not verified |

[^1]: Number of vCPU of the platform usually corresponds to the total number of vCPU of the bare metal instance. For a bare metal instance with 2x 24 cores CPU the platform_vcpu is: 2 (CPU units) x 24 (core units) x 2 ("threads" per core) = 96 vCPU.

[^2]: If the CPU is missing from the `cpu_specs.csv` (located at `boaviztapi/data/crowdsourcing/`), please consider to add it there as well to enrich the internal database.

### Missing values

Some values that are not required can be left empty if unknown and will be auto-completed by the API. Try to fill all columns as much as possible. 

### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. This can help modeling uncertain values like the weight of a power supply for instance. In the example above the default power supply weighs 2.99 kg, but can vary from 1 kg to 5 kg.
