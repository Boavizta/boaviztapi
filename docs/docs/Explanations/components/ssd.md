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

**The following variables can be [completed](../auto_complete.md)**

### density

if ```manufacturer``` is given, ```density``` can be retrieved from a fuzzy matching on our ssd repository.

## Manufacture impact

For one SSD the manufacture impact is:

$$
\text{SSD}_\text{manufacture}^\text{criteria} = (\text{SSD}_{\text{capacity}} / \text{SSD}_{\text{density}}) * \text{SSD}_\text{manufacture_die}^\text{criteria} + \text{SSD}_\text{manufacture_base}^\text{criteria}
$$

with:

| Constant                                        | Units       | Value    |
|-------------------------------------------------|-------------|----------|
| $\text{SSD}_\text{manufacture_die}^\text{gwp}$  | kgCO2eq/cm2 | 2.20     |
| $\text{SSD}_\text{manufacture_die}^\text{adp}$  | kgSbeq/cm2  | 6.30E-05 |
| $\text{SSD}_\text{manufacture_die}^\text{pe}$   | MJ/cm2      | 27.30    |
| $\text{SSD}_\text{manufacture_base}^\text{gwp}$ | kgCO2eq     | 6.34     |
| $\text{SSD}_\text{manufacture_base}^\text{adp}$ | kgSbeq      | 5.63E-04 |
| $\text{SSD}_\text{manufacture_base}^\text{pe}$  | MJ          | 76.90    |

_Note: If there are more than 1 SDD we multiply $\text{SSD}_\text{manufacture}^\text{criteria}$ by the number of SSD given in `units`._

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.