# Add a new cpu

This guide will help you add a new CPU into BoaviztAPI.

## Cloud instances CSV file

All available cpus are stored in a CSV file named `cpu_spec.csv` located at `boaviztapi/data/crowdsourcing/`. 

| Column name           | Required     | Description                                     | Example                                                  |
|-----------------------|--------------|-------------------------------------------------|----------------------------------------------------------|
| name                  | **Required** | CPU name                                        | AMD Ryzen 5 3600                                         |
| code_name             |              | Equivalent to family                            | Matisse                                                  |
| manufacturer          |              | CPU manufacturer                                | AMD                                                      |
| generation            |              | Generation full name                            | Ryzen 5 (Zen 2 (Matisse))                                |
| foundry               |              | Name of the foundry                             | TSMC                                                     |
| release_date          |              |                                                 | 2019-07-07                                               |
| frequency             |              | (in GHz)                                        | 3.6 GHz                                                  |
| tdp                   |              | Thermal design power  (in watt)                 | 65.0                                                     |
| cores                 |              | Number of physically cores                      | 6.0                                                      |
| transistors           |              | (in million)                                    | 3800                                                     |
| process_size          |              | process size of the main die area (in nm2)      | 7.0                                                      |
| die_size              |              | size of the main die area (in  mm²)             | 74                                                       |
| io_die_size           |              | size of the I/O die area when relevant(in  mm²) | 124                                                      |
| io_process_size       |              | process size of the I/O die area (in nm2)       | 12                                                       |
| total_die_size        |              | Total size of the die (in  mm²)[^1]             | 198.0                                                    |
| total_die_size_source |              | How did total_die_size has been calculated      | io_die_size (124 mm²) + die_size (74 mm²)                |
| model_range           |              | Name of the cpu range or brand                  | Ryzen 5                                                  |
| source                |              | Source of the above information                 | https://www.techpowerup.com/cpu-specs/ryzen-5-3600.c2132 |

 See on [GitHub](https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi/data/crowdsourcing/cpu_specs.csv)

[^1]: Either die_size or die_size + io_die_size when the chip has an I/O die area.