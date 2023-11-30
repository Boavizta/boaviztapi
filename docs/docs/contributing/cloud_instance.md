# Add a new cloud instance

This guide will help you add new cloud instances for a cloud provider that is already supported by BoaviztAPI.

## Cloud instances CSV file

To take full advantage of Boavizta's bottom-up methodology, we need to have precise information of the underlying hardware. **If the cloud instance is a Virtual Machine (VM), then we need the information of the bare metal instance.** Impacts of the bare metal instance will be split and attributed to the VM according to its specifications (e.g. bare metal is 32 vCPU, VM is 16 vCPU, then the embedded impacts of the VM will half (16/32) of the bare metal.)

All instances for one particular cloud provider are stored in a CSV file named after that cloud provider (e.g. `aws.csv` for AWS). These files are located at `boaviztapi/data/archetypes/cloud/`. See on [GitHub](https://github.com/Boavizta/boaviztapi/tree/main/boaviztapi/data/archetypes/cloud).

| Column name                   | Required     | Description                                                         | Example                   |
|-------------------------------|--------------|---------------------------------------------------------------------|---------------------------|
| id                            | **Required** | Instance identifier                                                 | c5.2xlarge                |
| manufacturer                  | **Required** | Cloud provider                                                      | AWS                       |
| CASE.type                     | **Required** | Type of enclosure (usually "rack")                                  | rack                      |
| year                          |              | Launch year                                                         | 2016                      |
| vcpu                          |              | Number of vCPU                                                      | 8                         |
| platform_vcpu                 |              | Number of vCPU of the platform                                      | 96                        |
| CPU.units                     |              | Number of physical CPU                                              | 2                         |
| CPU.name                      | **Required** | CPU name                                                            | Intel Xeon Platinum 8124M |
| instance.ram_capacity         |              | Instance RAM capacity (in GB)                                       | 16                        |
| RAM.units                     | **Required** | Number of RAM banks                                                 | 12                        |
| RAM.capacity                  | **Required** | RAM bank capacity                                                   | 16                        |
| SSD.units                     |              | Number of SSD disks                                                 | 1                         |
| SSD.capacity                  |              | Capacity of SSD disk (in GB)                                        | 512                       |
| HDD.units                     |              | Number of HDD disks                                                 | 1                         |
| HDD.capacity                  |              | Capacity of HDD disk (in GB)                                        | 4096                      |
| GPU.units                     |              | Number of GPU cards                                                 | 4                         |
| GPU.name                      |              | GPU name                                                            | NVIDIA A10G               |
| GPU.tdp                       |              | GPU TDP[^1] value (in Watt)                                         | 150                       |
| GPU.memory_capacity           |              | GPU memory capacity (in GB)                                         | 24                        |
| POWER_SUPPLY.units            | **Required** | Number of power supplies                                            | 2                         |
| POWER_SUPPLY.unit_weight      | **Required** | Power supply weight (in kg)                                         | 2.99;1;5                  |
| USAGE.instance_per_server     | **Required** | Number of instances hosted by the same platform                     | 12                        |
| USAGE.time_workload           | **Required** | Percentage of workload                                              | 50;0;100                  |
| USAGE.hours_life_time         | **Required** | Number of hours of life time                                        | 35040 _(=4 years)_        |
| USAGE.use_time_ratio          | **Required** | Proportion of the time the instance is being used                   | 1                         |
| USAGE.other_consumption_ratio | **Required** | Power consumption ratio of other components relative to RAM and CPU | 0.33;0.2;0.6              |
| USAGE.overcommited            |              | Platform is subject to over-commitment practices                    | False                     |
| Warnings                      |              | List of warnings separated by semi-colons (;)                       | RAM.capacity not verified |

### Compute

The compute part addresses the case of [CPU](#cpu) and [GPU](#gpu) components.

#### CPU

We need information about the number of vCPU of the VM instance (**vcpu**) and the bare metal instance (**platform_vcpu**). If you are adding a bare metal instance then, the values are equal: $\text{vcpu} = \text{platform_vcpu}$

Also, you will need to provide the name of the physical CPU (**CPU.name**), along with the number of CPU on the motherboard (**CPU.units**). Before adding the CPU name you must check, if the CPU is already registered in BoaviztAPI. To do so, you can manually search the CSV located at `boaviztapi/data/crowdsourcing/cpu_specs.csv` or search on [GitHub (recommended)](https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi/data/crowdsourcing/cpu_specs.csv). If the CPU does not exist, then you must follow this guide: [Add a CPU](cpu.md).

??? example "Example: add a `c5.2xlarge` AWS instance"
    
    Say we want to include the `c5.2xlarge` VM instance. 

    1. It has 8 vCPU according to the [AWS documentation](https://aws.amazon.com/ec2/instance-types/c5/). The bare metal version of that instance is the `c5.metal` with 96 vCPU. 
    2. The bare metal instance is equiped with 2x _Intel Xeon Platinum 8124M_ CPU. This CPU exists in BoaviztAPI.

    You will fill the information as follow:

    | id             | vcpu  | platform_vcpu | CPU.units | CPU.name                  |
    |----------------|-------|---------------|-----------|---------------------------|
    | **c5.2xlarge** | 8     | 96            | 2         | Intel Xeon Platinum 8124M |
    | **c5.metal**   | 96    | 96            | 2         | Intel Xeon Platinum 8124M |

#### GPU

### Memory (RAM)

### Storage

### Usage

### Missing values

Some values that are not required can be left empty if unknown and will be auto-completed by the API. Try to fill all columns as much as possible. 

### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. This can help modeling uncertain values like the weight of a power supply for instance. In the example above the default power supply weighs 2.99 kg, but can vary from 1 kg to 5 kg.


[^1]: Thermal Design Power (TDP)

[//]: # (Number of vCPU of the platform usually corresponds to the total number of vCPU of the bare metal instance. For a bare metal instance with 2x 24 cores CPU the platform_vcpu is: 2 &#40;CPU units&#41; x 24 &#40;core units&#41; x 2 &#40;"threads" per core&#41; = 96 vCPU.)

[//]: # (If the CPU is missing from the `cpu_specs.csv` &#40;located at `boaviztapi/data/crowdsourcing/`&#41;, please consider to add it there as well to enrich the internal database. For more information see [how to add a CPU]&#40;cpu.md&#41;.)

[//]: # (Not required if CPU.name is in `cpu_specs.csv`. Will be completed during the request treatment by the API based on the CPU name if the CPU have been added to `cpu_specs.csv`)

[//]: # (Usually the distribution of RAM modules is not known. In this case, take a hypothesis which respects: RAM.units*RAM.capacity = instance.ram_capacity * USAGE.instance_per_server and set the warning "RAM.capacity not verified")

[//]: # (Usually power supply duplicated so POWER_SUPPLY.units = 2. Usually POWER_SUPPLY.unit_weight is unknown, in that case use a range such as 2.99;1;5)

[//]: # (We usually consider that the number of instances on one platform is sized by the CPUs. So USAGE.instance_per_server = platform_vcpu / vcpu)

[//]: # (Should be a range between 0 and 100 &#40;50;0;100&#41; without valid justification)

[//]: # (In cloud environment a reserved instance is usually up 100% of the time so USAGE.use_time_ratio = 1)