# Cloud instances

## Characteristics

Cloud instance characteristics are pre-recorded as [archetypes](../archetypes.md). 
The API will complete the following characteristics depending on the cloud provider and cloud instance name given by the user :

| Name        | Unit  | Description                     | Example |
|-------------|-------|---------------------------------|---------|
| vcpu        | None  | Number of virtual CPUs          | 2       |
| memory      | GB    | RAM capacity                    | 2       |
| ssd_storage | GB    | ssd storage capacity            | 2       |
| hdd_storage | GB    | hdd storage capacity            | 2       |
| platform    | None  | Bare metal hosting the instance | 2       |
| usage       | None  | See usage                       | ..      |

To add a new cloud instance to the API please refer to the [cloud instance contribution guide](../../contributing/cloud_instance.md).

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

* For RAM :  $\text{RAM}_{\text{instance}}^{\text{embedded}} = \text{RAM}_{\text{server}}^{\text{embedded}} \times \frac{\text{RAM}_{\text{instance}}}{\text{RAM}_{\text{server}}}$


* For SSD storage
* For HDD storage
* For CPU and all other components

## Usage impacts

Usage impact of cloud instance are measured only from its [consumption profile](../consumption_profile.md).

As for embedded, usage impacts for a physical server are divided into the number of instances hosted by the server.

## Consumption profile

We use the same process as [described for the servers](../devices/server.md#consumption-profile) .
