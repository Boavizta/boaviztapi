# Add a new GPU

This guide will help you add a new GPU into BoaviztAPI.

## GPU specs CSV file

All available GPUs are stored in a CSV file named `gpu_specs.csv` located at `boaviztapi/data/crowdsourcing/`.

| Column name      | Required         | Description                                                              | Example              |
|------------------|------------------|--------------------------------------------------------------------------|----------------------|
| name             | **Required**     | Full commercial name of the GPU                                          | NVIDIA H100 SXM 80GB |
| unit             |                  | Number of GPU compute dies on the package                                | 1                    |
| number           |                  | Number of VRAM dies                                                      | 6                    |
| vram             |                  | Total VRAM capacity (in GB)                                              | 80                   |
| die_surface      |                  | Effective GPU die area **including losses** (in mm²)               | 2810.4               |
| pwb_surface      |                  | PCB (printed wiring board) surface area (in cm²)                        | 296.37               |
| distance_boat    |                  | Transport distance by boat from manufacturing site to market (in km)    | 19000                |
| distance_truck   |                  | Transport distance by truck from port to final destination (in km)      | 1000                 |
| distance_plane   |                  | Transport distance by plane, if applicable (in km)                      | 0                    |
| mass_casing      |                  | Mass of the casing / shroud (in kg)                                     | 0.789230             |
| mass_heatsink    |                  | Mass of the heatsink (in kg)                                            | 0.900770             |
| mass             |                  | Total mass of the GPU card (in kg)                                      | 1.690000             |

See on [GitHub](https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi/data/crowdsourcing/gpu_specs.csv)
