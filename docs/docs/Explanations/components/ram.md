# RAM

## Characteristics

| Name             | Unit   | Default value (default;min;max)  | Description                           | Example |
|------------------|--------|----------------------------------|---------------------------------------|---------|
| units            | None   | 1                                | RAM strip quantity                    | 2       |
| usage            | None   | See Usage                        | See usage                             | ..      |
| capacity         | GB     | 32;1;128                         | Capacity of a ram strip               | 12      |
| density          | GB/cm2 | (avg;min;max) in our dataset     | Size of the die per Go of a ram strip | 1.25    |
| process          | nm     | None                             | Engraving process (Architecture)      | 25      |
| manufacturer     | None   | None                             | Name of the ram manufacturer          | Samsung |
| model            | None   | None                             | ..                                    | ..      |


## Complete

**The following variables can be [completed](../auto_complete.md)**

### density

if ```process``` or/and ```manufacturer``` are given, ```density``` can be retrieved from a fuzzy matching on our ram repository.
If several ram matches the given ```process``` or/and ```manufacturer``` the average value is given and min and max value are used as ```min``` and ```max``` fields.

## Embedded impacts

### Impacts criteria

| Criteria | Implemented | Source                                                                                                                                                         | 
|----------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gwp      | yes         | [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| adp      | yes         | [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| pe       | yes         | [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| gwppb    | no          |                                                                                                                                                                |
| gwppf    | no          |                                                                                                                                                                |
| gwpplu   | no          |                                                                                                                                                                |
| ir       | no          |                                                                                                                                                                |
| lu       | no          |                                                                                                                                                                |
| odp      | no          |                                                                                                                                                                |
| pm       | no          |                                                                                                                                                                |
| pocp     | no          |                                                                                                                                                                |
| wu       | no          |                                                                                                                                                                |
| mips     | no          |                                                                                                                                                                |
| adpe     | no          |                                                                                                                                                                |
| adpf     | no          |                                                                                                                                                                |
| ap       | no          |                                                                                                                                                                |
| ctue     | no          |                                                                                                                                                                |
| ctuh_c   | no          |                                                                                                                                                                |
| ctuh_nc  | no          |                                                                                                                                                                |
| epf      | no          |                                                                                                                                                                |
| epm      | no          |                                                                                                                                                                |
| ept      | no          |                                                                                                                                                                |

### Impact factors

For one RAM bank the embedded impacts are:

$$
\text{RAM}_\text{embedded}^\text{criteria} = (\text{RAM}_{\text{capacity}} / \text{RAM}_{\text{density}}) * \text{RAM}_\text{embedded_die}^\text{criteria} + \text{RAM}_\text{embedded_base}^\text{criteria}
$$

with:

| Constant                                      | Units       | Value      |
|-----------------------------------------------|-------------|------------|
| $\text{RAM}_\text{embedded_die}^\text{gwp}$   | kgCO2eq/cm2 | 2.20       |
| $\text{RAM}_\text{embedded_die}^\text{adp}$   | kgSbeq/cm2  | 6.30E-05   |
| $\text{RAM}_\text{embedded_die}^\text{pe}$    | MJ/cm2      | 27.30      |
| $\text{RAM}_\text{embedded_base}^\text{gwp}$  | kgCO2eq     | 5.22       |
| $\text{RAM}_\text{embedded_base}^\text{adp}$  | kgSbeq      | 1.69E-03   |
| $\text{RAM}_\text{embedded_base}^\text{pe}$   | MJ          | 74.00      |

!!!info
    If there are more than 1 RAM bank we multiply $\text{RAM}_\text{embedded}^\text{criteria}$ by the number of RAM bank given in `units`._


## Usage impact

Both [power consumption](../usage/power.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

The power of a RAM strip (DIMM) is modelled per module rather than per GB: a DIMM draws roughly the same power whatever
its capacity, so the power per GB falls as DIMMs get bigger. The consumption profile of one RAM strip is of the form :

```consumption_profile(workload) = a * (idle_ratio + (1 - idle_ratio) * workload / 100)```

with ```a = dimm_base_power + dimm_power_per_gb * capacity``` the power of the strip at full load.

The workload is the same as the CPU's (```time_workload```).

### Determining the parameters

| Parameter         | Value | Source                                                                                                                                                                                                                                  |
|-------------------|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dimm_base_power   | 3 W   | Fitted to datasheet and measured values: Micron 128GB DDR5 RDIMM, 10 W ([product brief](https://assets.micron.com/adobe/assets/urn:aaid:aem:6ffd17ac-e709-469d-9473-a0a904681dd9/renditions/original/as/128gb-ddr5-rdimm-product-brief.pdf)); DDR5 64GB 5-6.5 W and DDR4 16GB ~4 W at saturated memory bandwidth ([arXiv 2309.05373](https://arxiv.org/abs/2309.05373)) |
| dimm_power_per_gb | 0.055 W/GB | Same as above |
| idle_ratio        | 0.7   | Share of DRAM power due to refresh and static power, [GreenDIMM (MICRO 2021)](https://doi.org/10.1145/3466752.3480089) |

For instance, at 50% workload a 32 GB strip draws ```(3 + 0.055 * 32) * 0.85 = 4.05 W``` (0.126 W/GB) and a 64 GB strip
```(3 + 0.055 * 64) * 0.85 = 5.54 W``` (0.087 W/GB).

Capacity is either given by the user or the default value is used.

### Cloud instances

The DIMM layout of cloud platforms is not published, so for cloud instances the capacity of the strips is not taken
from the platform but assumed from the memory type supported by the platform's CPU (see
```consumption_profile/ram/memory_type.csv```):

| Memory type | DIMM capacity assumed | CPU families (examples)                                                   |
|-------------|-----------------------|----------------------------------------------------------------------------|
| DDR3        | 16 GB                 | Sandy Bridge, Ivy Bridge                                                   |
| DDR4        | 32 GB                 | Haswell to Ice Lake, AMD Naples to Milan, Graviton, Graviton2 |
| DDR5        | 64 GB                 | Sapphire, Emerald and Granite Rapids, AMD Genoa, Graviton3 and Graviton4  |

DDR4 is used when the CPU family is unknown. The instance's memory is then counted as strips of that capacity.
