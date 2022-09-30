# SSD

SSD are Disk objects of ```type``` SSD.

## Characteristics

| Name          | Unit   | Default value | Description                  | Example |
|---------------|--------|---------------|------------------------------|---------|
| units         | None   | 1             | SSD quantity                 | 2       |
| usage         | None   | See Usage     | See usage                    | ..      |
| type          | None   | SSD           | "SSD"                        | SSD     |
| capacity      | Go     | 1000          | Capacity of a ssd disk       | 500     |
| density       | cm2/Go | 48.5          | cm2 per Go on a ssd wafer    | 48.5    |
| manufacturer  | None   | None          | Name of the CPU manufacturer | Samsung |
| model         | None   | None          | ..                           | ..      |


## Complete

**The following variables can be [completed](../complete.md)**

### density

if ```manufacturer``` is given, ```density``` can be retrieved from a fuzzy matching on our ssd repository.

## Manufacture impact

<h6>ssd<sub>manuf<sub><em>criteria</em></sub></sub> = ssd<sub>units</sub> x ( ( ssd<sub>size</sub> / ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + ssd<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With:

| Constant         | Units       | Value    |
|------------------|-------------|----------|
| ssdmanuf_diegwp  | kgCO2eq/cm2 | 2.20     |
| ssdmanuf_dieadp  | kgSbeq/cm2  | 6.30E-05 |
| ssdmanuf_diepe   | MJ/cm2      | 27.30    |
| ssdmanuf_basegwp | kgCO2eq     | 6.34     |
| ssdmanuf_baseadp | kgSbeq      | 5.63E-04 |
| ssdmanuf_basepe  | MJ          | 76.90    |


## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.