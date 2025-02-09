# Terminals & Peripherals

## General description

Terminals & peripherals may have several types (typically ```pro``` and ```perso```).

| Name            | Unit       | Default value | Description             | Example |
|-----------------|------------|---------------|-------------------------|---------|
| type            | None       | None          | A subcategory of device | perso   |


## Embedded impacts

Most embedded impacts are taken from the [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip) database. When the data comes from another source, it is specified.

| Criteria | Implemented | Source                                                                        | 
|----------|-------------|-------------------------------------------------------------------------------|
| gwp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| adp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| pe       | no          |                                                                               |
| gwppb    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| gwppf    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| gwpplu   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ir       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| lu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| odp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| pm       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| pocp     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| wu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| mips     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| adpe     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| adpf     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ap       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ctue     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ctuh_c   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ctuh_nc  | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| epf      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| epm      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |
| ept      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/documents/Negaoctet.zip)  |

## Usage impact

We use the classic [usage](../usage/usage.md) method. Default, minimal and maximal power consumptions are given for each device.

## Laptop

Laptop has two ```types```: ```pro``` and ```perso```.

### Embedded impacts

| Criteria | Unit               | pro      | perso    |
|----------|--------------------|----------|----------|
| gwp      | kgCO2eq            | 181.0    | 175.0    |
| gwpb     | kg CO2 eq.         | 0.318    | 0.377    |
| gwpf     | kg CO2 eq.         | 181.0    | 175.0    |
| gwplu    | kg CO2 eq.         | 3.37e-06 | 3.78e-06 |
| ir       | kg U235 eq.        | 73.6     | 75.5     |
| lu       | No dimension       | -56.0    | -59.5    |
| odp      | kg CFC-11 eq.      | 5.56e-05 | 5.05e-05 |
| pm       | Disease occurrence | 6.08e-06 | 5.85e-06 |
| pocp     | kg NMVOC eq.       | 0.46     | 0.45     |
| wu       | m3 eq.             | -812.0   | -820.0   |
| mips     | kg                 | 680.0    | 680.0    |
| adpe     | kg SB eq.          | 0.0086   | 0.008    |
| adpf     | MJ                 | 2410.0   | 2360.0   |
| ap       | mol H+ eq.         | 1.04     | 0.995    |
| ctue     | CTUe               | 2920.0   | 3050.0   |
| ctuh-c   | CTUh               | 3.98e-08 | 4.53e-08 |
| ctuh-nc  | CTUh               | 1.3e-06  | 1.08e-06 |
| epf      | kg P eq.           | -0.0126  | -0.0182  |
| epm      | kg N eq.           | 0.154    | 0.199    |
| ept      | mol N eq.          | 1.46     | 1.41     |

### Usage

#### Pro

| Name           | Unit      | Default values (default;min;max) | Description                                                      | Example |
|----------------|-----------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour | 75.0;50.0;100.0                  | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1        |                                  | Proportion of time the device is used during the given duration. | 0.2     |

#### Perso

| Name           | Unit        | Default values (default;min;max) | Description                                                      | Example  |
|----------------|-------------|----------------------------------|------------------------------------------------------------------|----------|
| avg_power      | Watt/hour   | 75.0;50.0;100.0                  | Average electrical consumption per hour                          | 1        |
| use_time_ratio | /1          |                                  | Proportion of time the device is used during the given duration. | 0.2      |


## Desktop

desktop has two ```types```: ```pro``` and ```perso```.

### Embedded impacts

| Criteria  | Unit               | pro       | perso     |
|-----------|--------------------|-----------|-----------|
| gwp       | kgCO2eq            | 277.0     | 277.0     |
| gwpb      | kg CO2 eq.         | 0.924     | 0.924     |
| gwpf      | kg CO2 eq.         | 275.0     | 275.0     |
| gwplu     | kg CO2 eq.         | 2.27e-07  | 2.27e-07  |
| ir        | kg U235 eq.        | 870.0     | 870.0     |
| lu        | No dimension       | -101.0    | -101.0    |
| odp       | kg CFC-11 eq.      | 6.24e-05  | 6.24e-05  |
| pm        | Disease occurrence | 9.6e-06   | 9.6e-06   |
| pocp      | kg NMVOC eq.       | 0.72      | 0.72      |
| wu        | m3 eq.             | -4490.0   | -4490.0   |
| mips      | kg                 | 1460.0    | 1460.0    |
| adpe      | kg SB eq.          | 0.00852   | 0.00852   |
| adpf      | MJ                 | 5110.0    | 5110.0    |
| ap        | mol H+ eq.         | 1.55      | 1.55      |
| ctue      | CTUe               | 4640.0    | 4640.0    |
| ctuh-c    | CTUh               | -2.83e-08 | -2.83e-08 |
| ctuh-nc   | CTUh               | 1.49e-06  | 1.49e-06  |
| epf       | kg P eq.           | -0.0852   | -0.0852   |
| epm       | kg N eq.           | 0.309     | 0.309     |
| ept       | mol N eq.          | 2.28      | 2.28      |

### Usage

#### Pro

| Name           | Unit          | Default values (default;min;max) | Description                                                      | Example |
|----------------|---------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour     | 175.0;100.0;450.0                | Average electrical consumption per hour                          |  1      |
| use_time_ratio | /1            |                                  | Proportion of time the device is used during the given duration. | 0.2     |


#### Perso

| Name           | Unit         | Default values (default;min;max) | Description                                                      | Example |
|----------------|--------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour    | 175.0;100.0;450.0                | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1           |                                  | Proportion of time the device is used during the given duration. | 0.2     |


## Tablet

### Embedded impacts

| Criteria   | Unit               | value    |
|------------|--------------------|----------|
| gwp        | kgCO2eq            | 75.9     |
| gwpb       | kg CO2 eq.         | 0.149    |
| gwpf       | kg CO2 eq.         | 75.9     |
| gwplu      | kg CO2 eq.         | 3.18e-06 |
| ir         | kg U235 eq.        | 32.4     |
| lu         | No dimension       | -1.34    |
| odp        | kg CFC-11 eq.      | 2.4e-05  |
| pm         | Disease occurrence | 2.62e-06 |
| pocp       | kg NMVOC eq.       | 0.196    |
| wu         | m3 eq.             | -84.6    |
| mips       | kg                 | 279.0    |
| adpe       | kg SB eq.          | 0.00375  |
| adpf       | MJ                 | 1000.0   |
| ap         | mol H+ eq.         | 0.465    |
| ctue       | CTUe               | 1540.0   |
| ctuh-c     | CTUh               | 1.79e-08 |
| ctuh-nc    | CTUh               | 6.99e-07 |
| epf        | kg P eq.           | -0.0028  |
| epm        | kg N eq.           | 0.063    |
| ept        | mol N eq.          | 0.609    |

### Usage

| Name           | Unit      | Default values (default;min;max) | Description                                                        | Example |
|----------------|-----------|----------------------------------|--------------------------------------------------------------------|---------|
| avg_power      | Watt/hour | 7.5;5.0;10.0                     | Average electrical consumption per hour                            | 1       |
| use_time_ratio | /1        |                                  | Proportion of time the device is used during the given duration.   | 0.2     |

## Smartphone

### Embedded impacts

| Criteria | Unit               | value      |
|----------|--------------------|------------|
| gwp      | kgCO2eq            | 84.0       |
| gwpb     | kg CO2 eq.         | 0.116      |
| gwpf     | kg CO2 eq.         | 84.0       |
| gwplu    | kg CO2 eq.         | 1.05e-06   |
| ir       | kg U235 eq.        | 13.7       |
| lu       | No dimension       | -2.27      |
| odp      | kg CFC-11 eq.      | 2.68e-05   |
| pm       | Disease occurrence | 2.7e-06    |
| pocp     | kg NMVOC eq.       | 0.198      |
| wu       | m3 eq.             | -107.0     |
| mips     | kg                 | 250.0      |
| adpe     | kg SB eq.          | 0.00205    |
| adpf     | MJ                 | 1110.0     |
| ap       | mol H+ eq.         | 0.48       |
| ctue     | CTUe               | 1340.0     |
| ctuh-c   | CTUh               | 1.66e-08   |
| ctuh-nc  | CTUh               | 5.65e-07   |
| epf      | kg P eq.           | -0.00295   |
| epm      | kg N eq.           | 0.105      |
| ept      | mol N eq.          | 0.61       |

### Usage

| Name           | Unit        | Default values (default;min;max) | Description                                                      | Example |
|----------------|-------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour   | 1.0;0.5;3.0                      | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1          |                                  | Proportion of time the device is used during the given duration. | 0.2     |

## Television

television has two ```types```: ```pro``` and ```perso```.

### Embedded impacts

| Criteria   | Unit               | pro      | perso    |
|------------|--------------------|----------|----------|
| gwp        | kgCO2eq            | 152.0    | 360.0    |
| gwpb       | kg CO2 eq.         | 0.737    | 1.56     |
| gwpf       | kg CO2 eq.         | 151.0    | 358.0    |
| gwplu      | kg CO2 eq.         | 6.43e-06 | 1e-05    |
| ir         | kg U235 eq.        | 330.0    | 960.0    |
| lu         | No dimension       | -224.0   | -339.0   |
| odp        | kg CFC-11 eq.      | 1.14e-05 | 1.86e-05 |
| pm         | Disease occurrence | 5.94e-06 | 1.39e-05 |
| pocp       | kg NMVOC eq.       | 0.469    | 1.06     |
| wu         | m3 eq.             | -808.0   | -920.0   |
| mips       | kg                 | 1000.0   | 1880.0   |
| adpe       | kg SB eq.          | 0.0249   | 0.0383   |
| adpf       | MJ                 | 3030.0   | 6610.0   |
| ap         | mol H+ eq.         | 0.944    | 2.38     |
| ctue       | CTUe               | 1730.0   | 5300.0   |
| ctuh-c     | CTUh               | 2.06e-08 | 5.21e-08 |
| ctuh-nc    | CTUh               | 2.18e-06 | 4.56e-06 |
| epf        | kg P eq.           | -0.017   | -0.0227  |
| epm        | kg N eq.           | 0.282    | 0.589    |
| ept        | mol N eq.          | 1.53     | 3.44     |

### Usage

#### Pro

| Name           | Unit       | Default values (default;min;max) | Description                                                      | Example |
|----------------|------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      |  Watt/hour | 300.0;17.0;1200.0                | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1         |                                  | Proportion of time the device is used during the given duration. | 0.2     |

#### Perso

| Name           | Unit        | Default values (default;min;max) | Description                                                      | Example |
|----------------|-------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour   | 300.0;17.0;1200.0                | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1          |                                  | Proportion of time the device is used during the given duration. | 0.2     |


## USB stick

### Embedded impacts

| Criteria   | Unit               | value    |
|------------|--------------------|----------|
| gwp        | kgCO2eq            | 6.25     |
| gwpb       | kg CO2 eq.         | 0.00454  |
| gwpf       | kg CO2 eq.         | 6.25     |
| gwplu      | kg CO2 eq.         | 9.15e-10 |
| ir         | kg U235 eq.        | 1.47     |
| lu         | No dimension       | -0.285   |
| odp        | kg CFC-11 eq.      | 2.35e-06 |
| pm         | Disease occurrence | 1.94e-07 |
| pocp       | kg NMVOC eq.       | 0.0138   |
| wu         | m3 eq.             | -2.02    |
| mips       | kg                 | 20.0     |
| adpe       | kg SB eq.          | 9.6e-05  |
| adpf       | MJ                 | 82.0     |
| ap         | mol H+ eq.         | 0.0346   |
| ctue       | CTUe               | 74.5     |
| ctuh-c     | CTUh               | 8.95e-10 |
| ctuh-nc    | CTUh               | 3.57e-08 |
| epf        | kg P eq.           | -0.00045 |
| epm        | kg N eq.           | 0.00448  |
| ept        | mol N eq.          | 0.0429   |

### Usage
| Name           | Unit                | Default values (default;min;max)     | Description                                                      | Example |
|----------------|---------------------|--------------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour           | 0.3;0.12;0.63                        | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1                  |                                      | Proportion of time the device is used during the given duration. | 0.2     |


## External SSD

### Embedded impacts

| Criteria  | Unit               |  value   |
|-----------|--------------------|----------|
| gwp       | kgCO2eq            | 109.0    |
| gwpb      | kg CO2 eq.         | 0.0765   |
| gwpf      | kg CO2 eq.         | 109.0    |
| gwplu     | kg CO2 eq.         | 3.89e-09 |
| ir        | kg U235 eq.        | 6.9      |
| lu        | No dimension       | -1.05    |
| odp       | kg CFC-11 eq.      | 4.56e-05 |
| pm        | Disease occurrence | 3.33e-06 |
| pocp      | kg NMVOC eq.       | 0.238    |
| wu        | m3 eq.             | -4.78    |
| mips      | kg                 | 264.0    |
| adpe      | kg SB eq.          | 0.000397 |
| adpf      | MJ                 | 1430.0   |
| ap        | mol H+ eq.         | 0.6      |
| ctue      | CTUe               | 1380.0   |
| ctuh-c    | CTUh               | 1.15e-08 |
| ctuh-nc   | CTUh               | 5.95e-07 |
| epf       | kg P eq.           | -0.00171 |
| epm       | kg N eq.           | 0.074    |
| ept       | mol N eq.          | 0.75     |

### Usage
| Name           | Unit                | Default values (default;min;max) | Description                                                      | Example |
|----------------|---------------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour           | 2.5;0.5;5.0                      | Average electrical consumption per hour                          |  1      |
| use_time_ratio | /1                  |                                  | Proportion of time the device is used during the given duration. | 0.2     |

## External HDD

### Embedded impacts

| Criteria   | Unit               | value    |
|------------|--------------------|----------|
| gwp        | kgCO2eq            | 15.8     |
| gwpb       | kg CO2 eq.         | 0.066    |
| gwpf       | kg CO2 eq.         | 15.7     |
| gwplu      | kg CO2 eq.         | 6.9e-09  |
| ir         | kg U235 eq.        | 19.7     |
| lu         | No dimension       | -3.09    |
| odp        | kg CFC-11 eq.      | 1.64e-06 |
| pm         | Disease occurrence | 6.5e-07  |
| pocp       | kg NMVOC eq.       | 0.051    |
| wu         | m3 eq.             | -488.0   |
| mips       | kg                 | 96.5     |
| adpe       | kg SB eq.          | 0.00234  |
| adpf       | MJ                 | 225.0    |
| ap         | mol H+ eq.         | 0.086    |
| ctue       | CTUe               | 344.0    |
| ctuh-c     | CTUh               | 2.65e-09 |
| ctuh-nc    | CTUh               | 2.51e-07 |
| epf        | kg P eq.           | -0.00165 |
| epm        | kg N eq.           | 0.0184   |
| ept        | mol N eq.          | 0.181    |

### Usage
| Name           | Unit          | Default values (default;min;max) | Description                                                        | Example |
|----------------|---------------|----------------------------------|--------------------------------------------------------------------|---------|
| avg_power      | Watt/hour     | 7.75;6.5;9.0                     | Average electrical consumption per hour                            | 1       |
| use_time_ratio | /1            |                                  | Proportion of time the device is used during the given duration.   | 0.2     |

## Monitor

### Embedded impacts

| Criteria   |  Unit              | value    |
|------------|--------------------|----------|
| gwp        | kgCO2eq            | 64.7     |
| gwpb       | kg CO2 eq.         | 0.309    |
| gwpf       | kg CO2 eq.         | 64.5     |
| gwplu      | kg CO2 eq.         | 2.83e-06 |
| ir         | kg U235 eq.        | 145.0    |
| lu         | No dimension       | -101.0   |
| odp        | kg CFC-11 eq.      | 4.95e-06 |
| pm         | Disease occurrence | 2.57e-06 |
| pocp       | kg NMVOC eq.       | 0.2      |
| wu         | m3 eq.             | -640.0   |
| mips       | kg                 | 423.0    |
| adpe       | kg SB eq.          | 0.0108   |
| adpf       | MJ                 | 1300.0   |
| ap         | mol H+ eq.         | 0.382    |
| ctue       | CTUe               | 477.0    |
| ctuh-c     | CTUh               | 4.57e-10 |
| ctuh-nc    | CTUh               | 5.93e-07 |
| epf        | kg P eq.           | -0.0108  |
| epm        | kg N eq.           | 0.109    |
| ept        | mol N eq.          | 0.65     |

### Usage
| Name           | Unit       | Default values (default;min;max) | Description                                                      | Example |
|----------------|------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      |  Watt/hour | 55.0;20.0;100.0                  | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1         |                                  | Proportion of time the device is used during the given duration. | 0.2     |


## Box

### Embedded impacts

| Criteria  | Unit               |  value    |
|-----------|--------------------|-----------|
| gwp       | kgCO2eq            | 36.1      |
| gwpb      | kg CO2 eq.         | 0.089     |
| gwpf      | kg CO2 eq.         | 36.0      |
| gwplu     | kg CO2 eq.         | 1.21e-08  |
| ir        | kg U235 eq.        | 135.0     |
| lu        | No dimension       | -46.3     |
| odp       | kg CFC-11 eq.      | 4.66e-06  |
| pm        | Disease occurrence | 1.27e-06  |
| pocp      | kg NMVOC eq.       | 0.087     |
| wu        | m3 eq.             | -422.0    |
| mips      | kg                 | 257.0     |
| adpe      | kg SB eq.          | 4.41e-05  |
| adpf      | MJ                 | 525.0     |
| ap        | mol H+ eq.         | 0.179     |
| ctue      | CTUe               | -42.8     |
| ctuh-c    | CTUh               | 9.6e-08   |
| ctuh-nc   | CTUh               | -3.29e-07 |
| epf       | kg P eq.           | -0.02     |
| epm       | kg N eq.           | 0.0375    |
| ept       | mol N eq.          | 0.25      |

### Usage
| Name           | Unit                         | Default values (default;min;max) | Description                                                      | Example |
|----------------|------------------------------|----------------------------------|------------------------------------------------------------------|---------|
| avg_power      | Watt/hour                    | 10.0;5.0;20.0                    | Average electrical consumption per hour                          | 1       |
| use_time_ratio | /1                           |                                  | Proportion of time the device is used during the given duration. | 0.2     |


## Smartwatch
In progress...

### Embedded impacts

| Criteria | Unit  | value  |
|----------|-------|--------|

### Usage

| Name       | Unit                         | Default values (default;min;max)  | Description                                   | Example |
|------------|------------------------------|-----------------------------------|-----------------------------------------------|---------|
| avg_power  | Watt/hour                    | 0.0;0.0;0.0                       | Average electrical consumption per hour       | 1       |


## VR headset

VR headset has two ```types```: ```lcd``` and ```oled```.

### Embedded impacts

| Criteria | Unit               | lcd          | oled      |
|----------|--------------------|--------------|-----------|
| gwp      | kgCO2eq            | 4.59e+01     | 8.94e+01  |
| gwpb     | kg CO2 eq.         | 8.83e-02     | 4.33e-01  |
| gwpf     | kg CO2 eq.         | 4.30e+02     | 8.89e+01  |
| gwplu    | kg CO2 eq.         | 9.55e-05     | 4.73e-08  |
| ir       | kg U235 eq.        | 1.54e+01     | 2.12e+02  |
| lu       | No dimension       | 1.71e+00     | 1.18e+00  |
| odp      | kg CFC-11 eq.      | 1.52e-05     | 8.39e-06  |
| pm       | Disease occurrence | 1.50e-06     | 3.30e-06  |
| pocp     | kg NMVOC eq.       | 1.15e-01     | 2.41e-01  |
| wu       | m3 eq.             | 1.27e+02     | 4.29e+02  |
| mips     | kg                 | 1.54e+02     | 3.03e+02  |
| adpe     | kg SB eq.          | 3.33e-03     | 4.54e-03  |
| adpf     | MJ                 | 6.11e+02     | 1.35e+03  |
| ap       | mol H+ eq.         | 2.64e-01     | 5.96e-01  |
| ctue     | CTUe               | 6.82e+02     | 1.68e+03  |
| ctuh-c   | CTUh               | 1.31e-06     | 5.00e-06  |
| ctuh-nc  | CTUh               | 6.84e-07     | 1.02e-06  |
| epf      | kg P eq.           | 7.00e-04     | 1.11e-04  |
| epm      | kg N eq.           | 3.74e-02     | 1.22e-01  |
| ept      | mol N eq.          | 3.69e-01     | 7.69e-01  |

### Usage

#### lcd

| Name             | Unit         | Default values (default;min;max) | Description                                                      | Example  |
|------------------|--------------|----------------------------------|------------------------------------------------------------------|----------|
| avg_power        | Watt/hour    | 692;692;692                      | Average electrical consumption per hour                          | 1        |
| use_time_ratio   | /1           | 0.01                             | Proportion of time the device is used during the given duration. | 0.2      |
| hours_life_time  | hours        | 43800                            | Life time of the device in hours                                 | 1000     |
 
#### oled

| Name            | Unit        | Default values (default;min;max) | Description                                                      | Example  |
|-----------------|-------------|----------------------------------|------------------------------------------------------------------|----------|
| avg_power       | Watt/hour   | 710;710;710                      | Average electrical consumption per hour                          | 1        |
| use_time_ratio  | /1          | 0.01                             | Proportion of time the device is used during the given duration. | 0.2      |
| hours_life_time | hours       | 43800                            | Life time of the device in hours                                 | 1000     |


## VR controller

### Embedded impacts

| Criteria | Unit               | value     |
|----------|--------------------|-----------|
| gwp      | kgCO2eq            | 4.22e+00  |
| gwpb     | kg CO2 eq.         | 1.97e-02  |
| gwpf     | kg CO2 eq.         | 4.20e+00  |
| gwplu    | kg CO2 eq.         | 4.14e-06  |
| ir       | kg U235 eq.        | 2.50e+00  |
| lu       | No dimension       | 5.73e-01  |
| odp      | kg CFC-11 eq.      | 7.66e-07  |
| pm       | Disease occurrence | 2.22e-07  |
| pocp     | kg NMVOC eq.       | 1.46e-02  |
| wu       | m3 eq.             | 3.99e+01  |
| mips     | kg                 | 5.47e+01  |
| adpe     | kg SB eq.          | 1.07e-03  |
| adpf     | MJ                 | 5.45e+01  |
| ap       | mol H+ eq.         | 4.28e-02  |
| ctue     | CTUe               | 5.11e+01  |
| ctuh-c   | CTUh               | 5.95e-08  |
| ctuh-nc  | CTUh               | 1.85e-07  |
| epf      | kg P eq.           | 9.87e-05  |
| epm      | kg N eq.           | 4.28e-03  |
| ept      | mol N eq.          | 4.49e-02  |

### Usage

#### lcd

| Name              | Unit         | Default values (default;min;max) | Description                                                      | Example  |
|-------------------|--------------|----------------------------------|------------------------------------------------------------------|----------|
| avg_power         | Watt/hour    | 7.90;7.90;7.90                   | Average electrical consumption per hour                          | 1        |
| use_time_ratio    | /1           | 0.01                             | Proportion of time the device is used during the given duration. | 0.2      |
| hours_life_time   | hours        | 43800                            | Life time of the device in hours                                 | 1000     |
