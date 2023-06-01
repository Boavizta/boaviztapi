# Server

## Characteristics

| Name         | Unit | Default value                                                 | Description    | Example |
|--------------|------|---------------------------------------------------------------|----------------|---------|
| usage        | None | See [server usage](../usage/usage.md)                         |                | ..      |
| cpu          | None | See [cpu](../components/cpu.md)                               |                | ..      |
| ram          | None | See [ram](../components/ram.md)                               |                | ..      |
| disk         | None | See [ssd](../components/ssd.md) & [hdd](../components/hdd.md) | SSD or HDD     | ..      |
| motherboard  | None | See [motherboard](../components/motherboard.md)               |                | ..      |
| power_supply | None | See [power_supply](../components/power_supply.md)             |                | ..      |
| assembly     | None | See [assembly](../components/assembly.md)                     | Assembly phase | ..      |
| case         | None | See [case](../components/case.md)                             | Enclosure      | ..      |


### Server usage 

In addition to the characteristics available for [usage](../usage/usage.md), you can use the following:

| Name                        | Unit           | Default value (default;min;max) | Description                                                         | Example |
|-----------------------------|----------------|---------------------------------|---------------------------------------------------------------------|---------|
| other_consumption_ratio     | None           | 0.33;0.2;0.6                    | Power consumption ratio of other components relative to RAM and CPU | 0.2     |
| hours_life_time             | None           | 35040                           | Lifespan of the element                                             | 3       |
| use_time_ratio              | /1             | 1                               | Proportion of time the instance is used during the given duration.  | 0.5     |


## Complete

The following components are [completed](../auto_complete.md) with the characteristics taken from the [archetype](../archetypes.md) :

* [CPU](../components/cpu.md)
* [RAM](../components/ram.md)
* [SSD](../components/ssd.md)
* [HDD](../components/hdd.md)
* [power supplies](../components/power_supply.md)
* [case](../components/case.md)

## Embedded impacts

### Impacts criteria

| Criteria | Implemented | Source                                                                                                                                                                                     | 
|----------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gwp      | yes         | Bottom-up approach based on [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| adpe     | yes         | Bottom-up approach based on [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| pe       | yes         | Bottom-up approach based on [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| gwppb    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| gwppf    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| gwpplu   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ir       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| lu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| odp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| pm       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| pocp     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| wu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| mips     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| adpf     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ap       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctue     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctuh_c   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctuh_nc  | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| epf      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| epm      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ept      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |

### Bottom-up approach

$$
\begin{equation}
\begin{aligned}
\text{server}_\text{embedded}^\text{criteria} & = \sum_{\set{\text{components}}}{\text{component}_
\text{embedded}^\text{criteria}} \\ \\
& = \text{cpu_units} * \text{CPU}_{embedded}^{criteria} \\
& \quad + \ \text{ram_units} * \text{RAM}_{embedded}^{criteria} \\
& \quad + \ \text{ssd_units} * \text{SSD}_{embedded}^{criteria} \\
& \quad + \ \text{hdd_units} * \text{HDD}_{embedded}^{criteria} \\
& \quad + \ \text{motherboard}_{embedded}^{criteria} \\
& \quad + \ \text{power_supply_units} * \text{power_supply}_{embedded}^{criteria} \\
& \quad + \ \text{assembly}_{embedded}^{criteria} \\
& \quad + \ \text{enclosure}_{embedded}^{criteria}
\end{aligned}
\end{equation}
$$

### Fix impact factors

| Criteria   | Unit               | value          |
|------------|--------------------|----------------|
| ir         | kg U235 eq.        | 2320.0         |
| lu         | No dimension       | -147.0         |
| odp        | kg CFC-11 eq.      | 0.00135        |
| pm         | Disease occurrence | 0.000113       |
| pocp       | kg NMVOC eq.       | 8.4            |
| wu         | m3 eq.             | -3710.0        |
| mips       | kg                 | 10600.0        |
| adpe       | kg SB eq.          | 0.0378         |
| adpf       | MJ                 | 51500.0        |
| ap         | mol H+ eq.         | 19.7           |
| ctue       | CTUe               | 48400.0        |
| ctuh-c     | CTUh               | 1.94e-07       |
| ctuh-nc    | CTUh               | 1.87e-05       |
| epf        | kg P eq.           | -0.258         |
| epm        | kg N eq.           | 2.94           |
| ept        | mol N eq.          | 27.0           |

## Usage impact

Both [power consumption](../usage/elec_conso.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

A server consumption profile is of the form :

$$
\text{CP}_{\text{component}} = \text{consumption_profile}_{\text{component}}
$$

$$
\text{CP}(\text{workload}) = (\text{CP}_{\text{CPU}}(\text{workload})
+ \text{CP}_{\text{RAM}}(\text{workload}))
* (1 + \text{other_consumption_ratio})
$$

$\text{CP}_{\text{CPU}}(\text{workload})$ and $\text{CP}_{\text{RAM}}(\text{workload})$ depend on the technical
characteristics of the RAM and CPU.
$\text{other_consumption_ratio}$ is used to account for the electrical consumption of the other components (other than RAM
and CPU).