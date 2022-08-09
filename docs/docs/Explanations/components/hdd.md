# HDD

HDD are Disk objects of ```type``` HDD.

## Characteristics

| Name          | Unit   | Default value | Description            | Example |
|---------------|--------|---------------|------------------------|---------|
| units         | None   | 1             | HDD quantity           | 2       |
| usage         | None   | See Usage     | See usage              | ..      |
| type          | None   | HDD           | "HDD"                  | HDD     |
| capacity      | Go     | 500           | Capacity of a HDD disk | 1000    |


## Manufacture impact

<h6>hdd<sub>manuf<sub><em>criteria</em></sub></sub> = hdd<sub>units</sub> x hdd<sub>manuf_unit<sub><em>criteria</em></sub></sub></h6>

With:

| Constant          | Unit    | Value    |
|-------------------|---------|----------|
| hddmanuf_unitgwp  | kgCO2eq | 31.10    |
| hddmanuf_unitadp  | kgSbeq  | 2.50E-04 |
| hddmanuf_unitpe   | MJ      | 276.00   |

## Usage impact

Only power consumption is implemented.