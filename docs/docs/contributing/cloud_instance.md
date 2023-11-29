# Add a new cloud instance

This guide will help you add new cloud instances for a cloud provider that is already supported by BoaviztAPI.

## Cloud instances CSV file

All instances for one particular cloud provider are stored in a CSV file named after that cloud provider (e.g. `aws.csv` for AWS). These files are located at `boaviztapi/data/archetypes/cloud/`. 

| Column name                   | Required     | Description                                                             | Example                   |
|-------------------------------|--------------|-------------------------------------------------------------------------|---------------------------|
| id                            | **Required** | Instance identifier                                                     | c5.2xlarge                |
| manufacturer                  | **Required** | Cloud provider                                                          | AWS                       |
| CASE.type                     | **Required** | Type of enclosure (usually "rack")                                      | rack                      |
| year                          |              | Launch year                                                             | 2016                      |
| vcpu                          |              | Number of vCPU                                                          | 8                         |
| platform_vcpu                 |              | Number of vCPU of the platform[^1]                                      | 96                        |
| CPU.units                     |              | Number of physical CPU                                                  | 2                         |
| CPU.name                      | **Required** | CPU name[^2]                                                            | Xeon Platinum 8124M       |
| CPU.core_units                | **Required** | Number of CPU cores per CPU[^3]                                         | 24                        |
| CPU.manufacturer              |              | CPU manufacturer[^3]                                                    | Intel                     |
| CPU.model_range               |              | CPU model range[^3]                                                     | Xeon Platinum             |
| CPU.family                    | **Required** | CPU family[^3]                                                          | Skylake                   |
| CPU.tdp                       | **Required** | CPU TDP (in Watt)[^3]                                                   | 240                       |
| CPU.manufacture_date          |              | CPU manufacture date[^3]                                                | 2016                      |
| instance.ram_capacity         |              | Instance RAM capacity (in GB)                                           | 16                        |
| RAM.units                     | **Required** | Number of RAM banks[^4]                                                 | 12                        |
| RAM.capacity                  | **Required** | RAM bank capacity[^4]                                                   | 16                        |
| SSD.units                     |              | Number of SSD disks                                                     | 1                         |
| SSD.capacity                  |              | Capacity of SSD disk (in GB)                                            | 512                       |
| HDD.units                     |              | Number of HDD disks                                                     | 1                         |
| HDD.capacity                  |              | Capacity of HDD disk (in GB)                                            | 4096                      |
| GPU.units                     |              | Number of GPU cards                                                     | 4                         |
| GPU.name                      |              | GPU name                                                                | NVIDIA A10G               |
| GPU.tdp                       |              | GPU TDP value (in Watt)                                                 | 150                       |
| GPU.memory_capacity           |              | GPU memory capacity (in GB)                                             | 24                        |
| POWER_SUPPLY.units            | **Required** | Number of power supplies[^5]                                            | 2                         |
| POWER_SUPPLY.unit_weight      | **Required** | Power supply weight (in kg)[^5]                                         | 2.99;1;5                  |
| USAGE.instance_per_server     | **Required** | Number of instances hosted by the same platform[^6]                     | 12                        |
| USAGE.time_workload           | **Required** | Percentage of workload[^7]                                              | 50;0;100                  |
| USAGE.hours_life_time         | **Required** | Number of hours of life time                                            | 35040 _(=4 years)_        |
| USAGE.use_time_ratio          | **Required** | Proportion of the time the instance is being used[^8]                   | 1                         |
| USAGE.other_consumption_ratio | **Required** | Power consumption ratio of other components relative to RAM and CPU[^9] | 0.33;0.2;0.6              |
| USAGE.overcommited            |              | Platform is subject to over-commitment practices                        | False                     |
| Warnings                      |              | List of warnings separated by semi-colons (;)                           | RAM.capacity not verified |

 See on [GitHub](https://github.com/Boavizta/boaviztapi/tree/main/boaviztapi/data/archetypes/cloud)

[^1]: Number of vCPU of the platform usually corresponds to the total number of vCPU of the bare metal instance. For a bare metal instance with 2x 24 cores CPU the platform_vcpu is: 2 (CPU units) x 24 (core units) x 2 ("threads" per core) = 96 vCPU.

[^2]: If the CPU is missing from the `cpu_specs.csv` (located at `boaviztapi/data/crowdsourcing/`), please consider to add it there as well to enrich the internal database. For more information see [how to add a CPU](cpu.md).

[^3]: Not required if CPU.name is in `cpu_specs.csv`. Will be completed during the request treatment by the API based on the CPU name if the CPU have been added to `cpu_specs.csv`

[^4]: Usually the distribution of RAM modules is not known. In this case, take a hypothesis which respects: RAM.units*RAM.capacity = instance.ram_capacity * USAGE.instance_per_server and set the warning "RAM.capacity not verified"

[^5]: Usually power supply duplicated so POWER_SUPPLY.units = 2. Usually POWER_SUPPLY.unit_weight is unknown, in that case use a range such as 2.99;1;5

[^6]: We usually consider that the number of instances on one platform is sized by the CPUs. So USAGE.instance_per_server = platform_vcpu / vcpu

[^7]: Should be a range between 0 and 100 (50;0;100) without valid justification

[^8]: In cloud environment a reserved instance is usually up 100% of the time so USAGE.use_time_ratio = 1


### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. This can help modeling uncertain values like the weight of a power supply for instance. In the example above the default power supply weighs 2.99 kg, but can vary from 1 kg to 5 kg.
