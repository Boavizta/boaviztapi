# SSD

SSD are Disk objects of ```type``` SSD.

## Characteristics

| Name         | Unit   | Default value                | Description                  | Example   |
|--------------|--------|------------------------------|------------------------------|-----------|
| units        | None   | 1                            | SSD quantity                 | 2         |
| usage        | None   | See Usage                    | See usage                    | ..        |
| type         | None   | SSD                          | "SSD"                        | SSD       |
| capacity     | Go     | 1000;100;5000                | Capacity of a ssd disk       | 500       |
| density      | GB/cm2 | (avg;min;max) in our dataset | GB per cm2 on a ssd wafer    | 48.5      |
| manufacturer | None   | None                         | Name of the CPU manufacturer | Samsung   |
| model        | None   | None                         | ..                           | ..        |
| layers       | None   | None                         | Number of layers             | 64        |


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

**The following variables can be [completed](../auto_complete.md)**

### density

if ```manufacturer``` is given, ```density``` can be retrieved from a fuzzy matching on our ssd repository. 
If several ssd matches the given ```manufacturer``` the average value is given and min and max value are used as ```min``` and ```max``` fields.


## Manufacture impact

For one SSD the embedded impact is:

$$
\text{SSD}_\text{embedded}^\text{criteria} = (\text{SSD}_{\text{capacity}} / \text{SSD}_{\text{density}}) * \text{SSD}_\text{embedded_die}^\text{criteria} + \text{SSD}_\text{embedded_base}^\text{criteria}
$$

with:

| Constant                                       | Units       | Value    |
|------------------------------------------------|-------------|----------|
| $\text{SSD}_\text{embedded_die}^\text{gwp}$    | kgCO2eq/cm2 | 2.20     |
| $\text{SSD}_\text{embedded_die}^\text{adp}$    | kgSbeq/cm2  | 6.30E-05 |
| $\text{SSD}_\text{embedded_die}^\text{pe}$     | MJ/cm2      | 27.30    |
| $\text{SSD}_\text{embedded_base}^\text{gwp}$   | kgCO2eq     | 6.34     |
| $\text{SSD}_\text{embedded_base}^\text{adp}$   | kgSbeq      | 5.63E-04 |
| $\text{SSD}_\text{embedded_base}^\text{pe}$    | MJ          | 76.90    |

!!!info
    If there are more than 1 SDD we multiply $\text{SSD}_\text{embedded}^\text{criteria}$ by the number of SSD given in `units`.

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.
