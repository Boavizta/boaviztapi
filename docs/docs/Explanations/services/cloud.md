# Cloud instances

## Characteristics

Cloud instance characteristics are pre-recorded as [archetypes](../archetypes.md). 
The API will complete the following characteristics depending on the cloud provider and cloud instance name given by the user :

| Name        | Unit  | Description                     | Example  |
|-------------|-------|---------------------------------|----------|
| vcpu        | None  | Number of virtual CPUs          | 2        |
| memory      | GB    | RAM capacity                    | 32       |
| ssd_storage | GB    | SSD storage capacity            | 500      |
| hdd_storage | GB    | HDD storage capacity            | 0        |
| platform    | None  | Bare metal hosting the instance | a1.metal |
| usage       | None  | See usage                       |          |

To add a new cloud instance to the API please refer to the [cloud instance contribution guide](../../contributing/cloud_instance.md).

### Cloud instance usage 

In addition to the characteristics available for [usage](../usage/usage.md), you can use the following:

| Name                        | Unit           | Default value (default;min;max) | Description                                                         | Example |
|-----------------------------|----------------|---------------------------------|---------------------------------------------------------------------|---------|
| other_consumption_ratio     | None           | 0.33;0.2;0.6                    | Power consumption ratio of other components relative to RAM and CPU | 0.2     |

## Embedded impacts

### Impacts criteria

| Criteria | Implemented | Source                                                                                                                                                                                     | 
|----------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gwp      | yes         | Bottom-up approach based on [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
| adp      | yes         | Bottom-up approach based on [Green Cloud Computing, 2021](https://www.umweltbundesamt.de/sites/default/files/medien/5750/publikationen/2021-06-17_texte_94-2021_green-cloud-computing.pdf) |
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
| adpe     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| adpf     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ap       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctue     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctuh_c   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ctuh_nc  | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| epf      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| epm      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |
| ept      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)                                                                                                               |

### Method

Embedded impacts of cloud instances are assessed based on the physical characteristics of the bare metal server hosting the instance (also named `platform` in this documentation). 
The API allocate a portion of the impacts of each component to the instance based on the ratio of the instance characteristics to the server characteristics :

* For RAM :  $\text{RAM}_{\text{instance}}^{\text{embedded}} = \text{RAM}_{\text{server}}^{\text{embedded}} \times \frac{\text{memory}_{\text{instance}}}{\text{RAM}_{\text{server}}}$
* For SSD storage : $\text{SSD}_{\text{instance}}^{\text{embedded}} = \text{SSD}_{\text{server}}^{\text{embedded}} \times \frac{\text{ssd_storage}_{\text{instance}}}{\text{ssd_storage}_{\text{server}}}$
* For HDD storage : $\text{HDD}_{\text{instance}}^{\text{embedded}} = \text{HDD}_{\text{server}}^{\text{embedded}} \times \frac{\text{hdd_storage}_{\text{instance}}}{\text{hdd_storage}_{\text{server}}}$
* For CPU and all other components : $\text{Component}_{\text{instance}}^{\text{embedded}} = \text{Component}_{\text{server}}^{\text{embedded}} \times \frac{\text{vCPU}_{\text{instance}}}{\text{vCPU}_{\text{server}}}$

The API will sum the embedded impacts of each component to get the embedded impacts of the instance :

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


When component impacts are not available, the API will use the generic impacts of the server and allocate the impacts to the instance based on the ratio of the instance vCPU to the server total vCPU : 

$\text{Instance}_{\text{embedded}} = \text{Server}_{\text{embedded}} \times \frac{\text{vCPU}_{\text{instance}}}{\text{vCPU}_{\text{server}}}$


## Usage impacts

Usage impact of cloud instance are measured only from its [consumption profile](../consumption_profile.md). 

## Consumption profile

A cloud instance consumption profile is of the form :

$$
\text{CP}_{\text{component}} = \text{consumption_profile}_{\text{component}}
$$

$$
\text{CP}_{\text{instance}}(\text{workload}) = (\text{CP}_{\text{CPU_server}}(\text{workload})
* \frac{\text{vCPU}_{\text{instance}}}{\text{vCPU}_{\text{server}}}
+ \text{CP}_{\text{RAM_server}}(\text{workload})
* \frac{\text{memory}_{\text{instance}}}{\text{RAM}_{\text{server}}})
* (1 + \text{other_consumption_ratio})
$$

$\text{CP}_{\text{CPU_server}}(\text{workload})$ and $\text{CP}_{\text{RAM_server}}(\text{workload})$ depend on the technical
characteristics of the RAM and CPU.
$\text{other_consumption_ratio}$ is used to account for the electrical consumption of the other components (other than RAM
and CPU).