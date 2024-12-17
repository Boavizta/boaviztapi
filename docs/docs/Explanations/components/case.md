# Case or Enclosure

## Characteristics

| Name       | Unit | Default value | Description                       | Example |
|------------|------|---------------|-----------------------------------|---------|
| units      | None | 1             | power supply quantity             | 2       |
| usage      | None | See Usage     | See usage                         | ..      |
| case_type  | None | rack          | Type of enclosure (blade or rack) | blade   |

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

The embedded impacts of a **rack server**:

$$
\text{enclosure}_\text{embedded}^\text{criteria} = \text{rack}_\text{embedded}^\text{criteria}
$$

The embedded impact of a **blade server**:

$$
\text{enclosure}_\text{embedded}^\text{criteria} = \text{blade}_\text{embedded}^\text{criteria}
+ \frac{\text{blade_enclosure}_\text{embedded}^\text{criteria}}{16}
$$

With :

| Constant                                                 | Unit    | Value      |
|----------------------------------------------------------|---------|------------|
| $\text{rack}_\text{embedded}^\text{gwp}$              | kgCO2eq | 150        |
| $\text{rack}_\text{embedded}^\text{adp}$              | kgSbeq  | 2.02E-02   |
| $\text{rack}_\text{embedded}^\text{pe}$               | MJ      | 2 200.00   |
| $\text{blade}_\text{embedded}^\text{gwp}$             | kgCO2eq | 30.90      |
| $\text{blade}_\text{embedded}^\text{adp}$             | kgSbeq  | 6.72E-04   |
| $\text{blade}_\text{embedded}^\text{pe}$              | MJ      | 435.00     |
| $\text{blade_enclosure}_\text{embedded}^\text{gwp}$   | kgCO2eq | 880.00     |
| $\text{blade_enclosure}_\text{embedded}^\text{adp}$   | kgSbeq  | 4.32E-01   |
| $\text{blade_enclosure}_\text{embedded}^\text{pe}$    | MJ      | 12 700.00  |

## Usage impacts

Only [power consumption](../usage/power.md) is implemented. In most cases, enclosure doesn't consume electricity.
