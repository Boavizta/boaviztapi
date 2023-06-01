# Cloud instances

## Characteristics

In addition to the characteristics available for a [server](../devices/server.md), you can use the following:

| Name       | Unit | Default value                        | Description | Example  |
|------------|------|--------------------------------------|-------------|----------|
| usage      | None | See [cloud usage](../usage/usage.md) |             | ..       |


### Cloud usage

In addition to the characteristics available for [server usage](../devices/server.md), you can use the following:

| Name                       | Unit           | Default value | Description                                                       | Example |
|----------------------------|----------------|---------------|-------------------------------------------------------------------|---------|
| instance_per_server        | None           | None          | See usage                                                         | 10      |
| hours_life_time            | hours          | 35040         | Lifespan of the cloud element                                     | 2       |
| use_time_ratio             | /1             | 1             | Proportion of time the device is used during the given duration.  | 0.5     |



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

### Method

Embedded impacts of cloud instances correspond to the impact of the physical [server](server.md) hosting the instance
divided by the number of instances hosted on the server.

$$
\text{cloud_instance}_\text{embedded}^\text{criteria} = \frac{\text{server}_
\text{embedded}^\text{criteria}}{\text{instances_per_server}}
$$

Components configuration are never sent by the user but pre-recorded as an [archetype](../archetypes.md).

## Usage impacts

Usage impact of cloud instance are measured only from its [consumption profile](../consumption_profile.md).

As for embedded, usage impacts for a physical server are divided into the number of instances hosted by the server.

## Consumption profile

We use the same process as [described for the servers](server.md#consumption-profile) .
