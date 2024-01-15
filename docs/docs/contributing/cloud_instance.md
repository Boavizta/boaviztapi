# Add a new cloud instance

This guide will help you add new cloud instances for a cloud provider that is already supported by BoaviztAPI.

## Cloud instances CSV file

To add cloud instances for a cloud provider, you will need to create a new CSV file using the same name as `provider.name` (e.g. `aws.csv`). The file must be created in the same location as the `providers.csv` file. You will need to have the exact same columns in the new CSV file compared to others. You can copy and paste the content of already existent list of instances from another cloud provider and remove all rows, but the first one.

| Column name | Required     | Unit  | Description                      | Example    |
|-------------|--------------|-------|----------------------------------|------------|
| id          | **Required** |       | Instance identifier              | c5.2xlarge |
| vcpu        | **Required** | unit  | Number of vCPU                   | 8          |
| memory      | **Required** | GB    | RAM quantity                     | 32         |
| ssd_storage |              | GB    | SSD storage quantity (can be 0)  | 200        |
| hdd_storage |              | GB    | HDD storage quantity (can be 0)  | 500        |
| gpu_units   |              | unit  | GPU quantity (not supported yet) | 2          |
| platform    | **Required** |       |                                  | 96         |


### Platform

The platform is the bare metal server that host the instance. Since we compute the impacts of the instance as a portion of the bare metal server, we need to know its architecture. 

The `platform` field must match one of the `id` of the available server archetypes. You can either use :

* a generic server among the server archetypes that are already supported by BoaviztAPI. You can find the list of supported platforms in the `servers.csv` file located at `boaviztapi/data/archetypes/servers.csv` or by requesting the list of server archetypes using the API endpoint `/v1/server/archetypes`.
* add a new platform to the `platforms.csv` file. See [Add a new server archetype](server.md).

!!! note
    It is often impossible to find the exact architecture of the bare metal server. When so use a generic server architecture that matches the instance purpose (storage, compute, memory etc.)


### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. For example, if the value is `default;2;8`, it means that the default value is `2` and the range is from `2` to `8`. If the value is `2;1;4`, it means that the default value is `2` and the range is from `1` to `2`.