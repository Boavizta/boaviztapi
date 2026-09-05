# Add a new cloud instance

This guide will help you add new cloud instances for a cloud provider that is already supported by BoaviztAPI.

## Cloud instances CSV file

To add cloud instances for a cloud provider, you will need to create a new CSV file using the same name as `provider.name` (e.g. `aws.csv`). The file must be created in the same location as the `providers.csv` file. You will need to have the exact same columns in the new CSV file compared to others. You can copy and paste the content of already existent list of instances from another cloud provider and remove all rows, but the first one.

| Column name | Required     | Unit  | Description                      | Example     |
|-------------|--------------|-------|----------------------------------|-------------|
| id          | **Required** |       | Instance identifier              | c5.12xlarge |
| vcpu        | **Required** | unit  | Number of vCPU                   | 48          |
| memory      | **Required** | GB    | RAM quantity                     | 96          |
| ssd_storage |              | GB    | SSD storage quantity (can be 0)  | 0           |
| hdd_storage |              | GB    | HDD storage quantity (can be 0)  | 0           |
| gpu_units   |              | unit  | GPU quantity [^1]                | 1           |
| platform    | **Required** |       |                                  | c5.metal    |

[^1]: May be fractional (`0.125`) for instances that share a partitioned GPU.
See [GPU units](#gpu-units).


### Platform

The platform is the bare metal server that host the instance. Since we compute the impacts of the instance as a portion of the bare metal server, we need to know its architecture. 

The `platform` field must match one of the `id` of the available server archetypes. You can either use :

* a generic server among the server archetypes that are already supported by BoaviztAPI. You can find the list of supported platforms in the `servers.csv` file located at `boaviztapi/data/archetypes/servers.csv` or by requesting the list of server archetypes using the API endpoint `/v1/server/archetypes`.
* add a new platform to the `platforms.csv` file. See [Add a new server archetype](server.md).

!!! note
    It is often impossible to find the exact architecture of the bare metal server. When so use a generic server architecture that matches the instance purpose (storage, compute, memory etc.)


### GPU units

`gpu_units` is the number of GPUs the instance is sold with. The API allocates the
platform's GPU embedded impacts by `gpu_units / GPU.units`, so the two files have to
agree:

* `gpu_units` must not exceed the `GPU.units` of the platform, otherwise the instance
  is allocated more than the whole host's GPU impact.
* If `gpu_units` is set, the platform must declare a `GPU.units` greater than 0 and a
  `GPU.name`. A platform with `GPU.units = 0` has no GPU at all as far as the API is
  concerned, and the instance is reported with no GPU impact.
* Leave it at `0` for an instance sold without a GPU, even when the platform has some.

Fractional values are allowed, for instances that share a GPU partitioned with vGPU or
MIG. Use the fraction of a whole card, not a count of slices: an instance getting an
eighth of one GPU is `0.125`. The commercial description of the slice belongs on the
platform row, in `GPU.name` and `GPU.vram`.

You can check `gpu_units` against the platforms with:

```bash
poetry run python3 boaviztapi/data/utils/scripts/check_references.py
```

### Value ranges

Some values can be inputted using ranges like the following: `default;min;max`. For example, if the value is `2;1;8`, it means that the default value is `2` and the range is from `1` to `8`.
