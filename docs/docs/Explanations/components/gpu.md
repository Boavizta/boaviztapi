# GPU

## Characteristics

| Name             | Unit | Default value              | Description                                                          | Example              |
|------------------|------|----------------------------|----------------------------------------------------------------------|----------------------|
| units            | None | 1                          | Number of GPUs (see `gpus_per_card`)                                 | 2                    |
| usage            | None | See Usage                  | See usage                                                            | ..                   |
| name             | None | None                       | Full commercial name of the GPU                                      | NVIDIA H100 SXM 80GB |
| weight           | kg   | 1.69                       | Total mass of the GPU card                                           | 1.69                 |
| heatsink_weight  | kg   | 0.90                       | Mass of the heatsink                                                 | 0.90                 |
| casing_weight    | kg   | 0.79                       | Mass of the casing / shroud                                          | 0.79                 |
| gpu_surface      | mm²  | 814 (effective)            | Effective GPU die area including wafer losses                        | 2810.4               |
| vram             | GB   | 80                         | Total VRAM capacity of the card                                      | 80                   |
| vram_dies        | None | 6                          | Number of VRAM dies                                                  | 6                    |
| vram_surface     | mm²  | computed                   | Total effective VRAM die area including wafer losses                 | 744.0                |
| pwb_surface      | cm²  | 296                        | PCB surface area                                                     | 296.37               |
| pwb_weight       | kg   | None                       | Mass of the PCB                                                      | 0.2                  |
| tdp              | W    | 700                        | Board power of one GPU card (TDP)                                    | 700                  |
| gpus_per_card    | None | 1                          | Number of GPUs on one card, e.g. 2 for a Tesla M60                   | 2                    |
| transport_boat   | km   | 19000                      | Distribution distance by boat                                        | 19000                |
| transport_truck  | km   | 1000                       | Distribution distance by truck                                       | 1000                 |
| transport_plane  | km   | 0                          | Distribution distance by plane                                       | 0                    |

## Complete

**The following [completion](../auto_complete.md) strategies can be used.**

### Completion from GPU `name`

If a GPU `name` is provided, the following attributes can be retrieved via fuzzy matching on the GPU name repository:

- `vram`, `vram_dies`
- `gpu_surface` (already the effective area — used as-is)
- `pwb_surface`
- `weight`, `heatsink_weight`, `casing_weight`
- `transport_boat`, `transport_truck`, `transport_plane`
- `tdp`, `gpus_per_card`

!!!warning
    The GPU name repository is not exhaustive, and the fuzzy match may return a different GPU than the one specified if the name is ambiguous or misspelled. The matching threshold is configurable via `BOAVIZTA_GPU_NAME_FUZZYMATCH_THRESHOLD` in the [config](../../config.md). You can contribute new GPU models by following the [contributing guide](../../contributing/gpu.md).

### Completion of `vram_surface`

If `vram_surface` is not set, it is computed from `vram` and `vram_dies`:

$$
\text{die\_area} = \frac{\text{vram} \times 15.5}{\text{vram\_dies}}
$$

$$
\text{vram\_surface} = \text{effective\_area}(\text{die\_area}) \times \text{vram\_dies}
$$

where $\text{effective\_area}$ accounts for wafer losses and die yield using the standard circular wafer model.

### Completion of `gpu_surface`

If `gpu_surface` is not set and not completed from name, the archetype default value (already expressed as effective area) is used.

## Embedded impacts

### Impact criteria

| Criteria  | Implemented |
|-----------|-------------|
| gwp       | yes         |
| adp       | yes         |
| pe        | yes         |
| gwppb     | no          |
| gwppf     | no          |
| gwpplu    | no          |
| ir        | yes         |
| lu        | yes         |
| odp       | yes         |
| pm        | yes         |
| pocp      | yes         |
| wu        | yes         |
| mips      | yes         |
| adpe      | no          |
| adpf      | yes         |
| ap        | yes         |
| ctue      | yes         |
| ctuh_c    | no          |
| ctuh_nc   | no          |
| epf       | no          |
| epm       | no          |
| ept       | yes         |
| fw        | no          |
| fe        | no          |

### Impact formula

The total embedded impact of one GPU card is the sum of contributions from each sub-component:

$$
\text{GPU}_\text{embedded}^\text{criteria} =
  \text{impact}^\text{casing}
+ \text{impact}^\text{heatsink}
+ \text{impact}^\text{pwb}
+ \text{impact}^\text{gpu\_die}
+ \text{impact}^\text{vram}
+ \text{impact}^\text{upstream\_transport}
+ \text{impact}^\text{boat}
+ \text{impact}^\text{truck}
+ \text{impact}^\text{plane}
+ \text{impact}^\text{end\_of\_life}
$$

Each sub-component impact uses a dedicated impact factor from the factor database:

- **Casing / heatsink**: factor × mass (kg)
- **PWB**: factor × pcb surface (cm²)
- **GPU die**: factor × effective die area (mm²)
- **VRAM**: factor × effective total VRAM die area (mm²)
- **Upstream transport**: factor × total card weight (kg)
- **Distribution transport** (boat / truck / plane): factor × distance (km) × total card weight (kg)
- **End of life**: factor × total card weight (kg)

!!!info
    The characteristics above describe a whole card. The embedded impact of one card is multiplied by
    `units / gpus_per_card`, the number of cards: providers count the GPUs of a dual-GPU card such as the
    Tesla M60 separately, so `units` is a number of GPUs.

## Usage impacts

Power consumption is based on the [usage](../usage/power.md) methodology. The GPU's workload and use time ratio are taken from the usage parameters.

`avg_power` is the average power of one GPU. When it is not given, it is modelled from the `tdp`, linearly from an
idle power of 10% of the TDP to the full TDP. The idle share is in line with the minimum and maximum powers of the
[Cloud Carbon Footprint GPU methodology](https://www.cloudcarbonfootprint.org/docs/methodology/#graphic-processing-units-gpus):

$$
\text{P}_{\text{GPU}}(\text{workload}) = \frac{\text{tdp}}{\text{gpus_per_card}} \times (0.1 + 0.9 \times \frac{\text{workload}}{100})
$$

The workload is the GPU's own `time_workload`, 65% by default. It does not follow the `time_workload` of a server or
cloud instance, which describes its CPU: GPUs for AI workloads run at 60 to 70% at cloud providers, according to
[Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect).
Total power is $\text{P}_{\text{GPU}} \times \text{units}$.
