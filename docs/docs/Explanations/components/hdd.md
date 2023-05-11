# HDD

HDD are Disk objects of ```type``` HDD.

## Characteristics

| Name          | Unit   | Default value | Description            | Example |
|---------------|--------|---------------|------------------------|---------|
| units         | None   | 1             | HDD quantity           | 2       |
| usage         | None   | See Usage     | See usage              | ..      |
| type          | None   | HDD           | "HDD"                  | HDD     |
| capacity      | Go     | None          | Capacity of a HDD disk | 1000    |

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

The HDD disk manufacturing impact is considered as a constant.

| Constant                                      | Unit    | Value    |
|-----------------------------------------------|---------|----------|
| $\text{HDD}_{\text{embedded}}^{\text{gwp}}$   | kgCO2eq | 31.10    |
| $\text{HDD}_{\text{embedded}}^{\text{adp}}$   | kgSbeq  | 2.50E-04 |
| $\text{HDD}_{\text{embedded}}^{\text{pe}}$    | MJ      | 276.00   |

!!!info
    If there are more than 1 HDD we multiply $\text{HDD}_\text{embedded}^\text{criteria}$ by the number of HDD given in `units`.

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.