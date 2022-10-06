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

The HDD disk manufacturing impact is considered as a constant.

| Constant                                       | Unit    | Value    |
|------------------------------------------------|---------|----------|
| $\text{HDD}_{\text{manufacture}}^{\text{gwp}}$ | kgCO2eq | 31.10    |
| $\text{HDD}_{\text{manufacture}}^{\text{adp}}$ | kgSbeq  | 2.50E-04 |
| $\text{HDD}_{\text{manufacture}}^{\text{pe}}$  | MJ      | 276.00   |

_Note: If there are more than 1 HDD we multiply $\text{HDD}_\text{manufacture}^\text{criteria}$ by the number of HDD
given in `units`._

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.