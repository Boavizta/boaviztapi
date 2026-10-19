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
| $\text{SSD}_\text{embedded_base}^\text{pe}$    | MJ          | 73.98    |

!!!info
    If there are more than 1 SDD we multiply $\text{SSD}_\text{embedded}^\text{criteria}$ by the number of SSD given in `units`.

## Usage impact

Only [power consumption](../usage/power.md) is implemented.

When part of a [server](../devices/server.md) or a [cloud instance](../services/cloud.md), each drive is assumed to draw a constant 8 W (min 2 W, max 20 W), independently of the workload. Enterprise NVMe drives idle at about 3.5 to 5 W and average about 8 to 14 W when active, depending on I/O, which the API does not model.

Sources: [Samsung PM9A3 specifications](https://www.avadirect.com/1-92TB-PM9A3-7mm-6800-4000-MB-s-V-NAND-PCIe-4-0-x4-NVMe-U-2-2-5-Inch-1-0-DWPD-SSD/Product/14705654), [Kanichai, Doekemeijer et al. (IISWC 2026)](https://atlarge-research.com/pdfs/2026-iiswc-nvme-energy.pdf), [LBNL, 2024 United States Data Center Energy Usage Report](https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf) (about 11 W per NVMe drive).
