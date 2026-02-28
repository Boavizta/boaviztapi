# Add a new server archetype

This guide will help you add a new server to the server archetypes. To learn more about server archetypes, please refer to the [archetypes documentation](../Explanations/archetypes.md).

## Server archetypes CSV file

All available servers are stored in a CSV file named `servers.csv` located at `boaviztapi/data/archetypes/servers.csv`.

| Column name                   | Required      | Unit  | Description                      | Example                 |
|-------------------------------|---------------|-------|----------------------------------|-------------------------|
| id                            | **Required**  |       | Server identifier                | platform_compute_medium |
| manufacturer                  |               |       | Server manufacturer              |                         |
| case_type                     | **Required**  |       | Server case type                 | rack                    |
| CPU.units                     | **Required**  | unit  | Number of CPU                    | 2                       |
| CPU.name [^1]                 |               |       | CPU name                         |                         |
| CPU.core_units                |               | unit  | Number of CPU cores per CPU      | 24                      |
| CPU.die_size_per_core         |               | mm²   | Die size per CPU core            | 8                       |
| CPU.die_size                  |               | mm²   | Die size per CPU                 | 500                     |
| CPU.tdp                       |               | Watt  | Thermal design power  (in watt)  | 150                     |
| CPU.vcpu                      |               | unit  | Number of vCPU per CPU           | 32                      |
| RAM.units                     | **Required**  | unit  | Number of RAM                    | 1                       |
| RAM.capacity                  |               | GB    | RAM quantity                     | 1000                    |
| SSD.units                     | **Required**  | unit  | Number of SSD                    | 0                       |
| SSD.capacity                  |               | GB    | SSD storage quantity             | 0                       |
| HDD.units                     | **Required**  | unit  | Number of HDD                    | 0                       |
| HDD.capacity                  |               | GB    | HDD storage quantity             | 0                       |
| GPU.units                     | **Required**  | unit  | GPU quantity (not supported yet) | 0                       |
| GPU.name                      |               |       | GPU name                         |                         |
| GPU.vram                      |               | GB    | GPU memory capacity              |                         |
| POWER_SUPPLY.units            | **Required**  | unit  | Number of power supply[^2]       | 2                       |
| POWER_SUPPLY.unit_weight      | **Required**  | kg    | Power supply weight[^2]          | 2.99;1;5                |
| USAGE.time_workload           | **Required**  | %     | Time workload [^3]               | 50;0;100                |
| USAGE.use_time_ratio          | **Required**  | /1    | Use time ratio[^4]               | 1                       |
| USAGE.hours_life_time         | **Required**  | hours | Hours life time                  | 35040                   |
| USAGE.other_consumption_ratio | **Required**  | /1    | Other consumption ratio          | 0.33                    |
| WARNINGS                      |               |       | Warnings                         |                         |

[^1]: If CPU.name is set and the CPU is available in [cpu_specs.csv](./cpu.md), you do not need to fill in the other CPU attributes. The API will complete them based on the CPU.name.

[^2]: (Usually power supply duplicated so POWER_SUPPLY.units = 2. Usually POWER_SUPPLY.unit_weight is unknown, in that case use a range such as 2.99;1;5)

[^3]: (Should be a range between 0 and 100 (50;0;100) without valid justification)

[^4]: (Should be 100% without valid justification so USAGE.use_time_ratio = 1)

### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. For example, if the value is `4;2;8`, it means that the default value is `4` and the range is from `2` to `8`.
