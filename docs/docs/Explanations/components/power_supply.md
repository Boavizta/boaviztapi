# Power supply

## Characteristics

| Name               | Unit | Default value (default;min:max) | Description                 | Example |
|--------------------|------|---------------------------------|-----------------------------|---------|
| units              | None | 1                               | power supply quantity       | 2       |
| usage              | None | See Usage                       | See usage                   | ..      |
| unit_weight        | kg   | 2.99;1;5                        | weight of the power supply  | 5       |

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

For one power supply the embedded impact is:

$$
\text{power_supply}_\text{embedded}^\text{criteria} = \text{power_supply}_\text{unit_weight} * \text{power_supply}_
\text{embedded_weight}^\text{criteria}
$$

with :

| Constant                                                 | Unit       | Value    |
|----------------------------------------------------------|------------|----------|
| $\text{power_supply}_\text{embedded_weight}^\text{gwp}$  | kgCO2eq/kg | 24.30    |
| $\text{power_supply}_\text{embedded_weight}^\text{adp}$  | kgSbeq/kg  | 8.30E-03 |
| $\text{power_supply}_\text{embedded_weight}^\text{pe}$   | MJ/kg      | 352.00   |

!!!info
    If there are more than 1 power we multiply $\text{power_supply}_\text{embedded}^\text{criteria}$ by the number of power supply given in `units`._

## Usage impact

Only [power consumption](../usage/power.md) is implemented.
This shouldn't be used in most cases since the electricity consume by a power supply is consume on behalf of other
components.