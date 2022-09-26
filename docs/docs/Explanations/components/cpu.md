# CPU

## Characteristics

| Name              | Unit | Default value | Description                                   | Example          |
|-------------------|------|---------------|-----------------------------------------------|------------------|
| units             | None | 1             | CPU quantity                                  | 2                |
| usage             | None | See Usage     | See usage                                     | ..               |
| core_units        | None | 24            | Number of core on one CPU                     | 12               |
| die_size          | mm2  | None          | Size of the die                               | 2900             |
| manufacturer      | None | Intel         | Name of the CPU manufacturer                  | AMD              |
| die_size_per_core | mm2  | 0.245         | Size of the die divided by the number of core | 0.245            |
| model_range       | None | Xeon Platinum | Name of the cpu range or brand                | i7               |
| family            | None | Skylake       | Name of the architectural family (Generation) | Naple            |
| name              | None | None          | Complete commercial name of the CPU           | Intel Core i7-1065 |
| TDP               | Watt | None          | Thermal Design Point                          | 250              |


## Complete

**The following variables can be [completed](complete.md)**

### die_size_per_core and core_units

if ```die_size``` and ```core_units``` are given :

```die_size_per_core = core_units/die_size```

Otherwise, if ```family``` or/and ```core_units``` are given, ```die_size_per_core``` can be retrieved from a fuzzy matching on our cpu repository.
If several cpu matches the given ```family``` and/or ```core_units``` the maximizing value is given (in terms of impacts).

If no cpu is found either because the cpu is unknown or not enough data have been given by the user the default data are used.

### model_range and family

if ```name``` is given, ```model_range``` and ```family``` can be retrieved from a fuzzy matching on our cpu name repository.

## Manufacture impact

<h6>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>units<sub></sub></sub> x ( ( cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0,491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + cpu<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

with:

| Constant         | Units       | Value    |
|------------------|-------------|----------|
| cpumanuf_diegwp  | kgCO2eq/cm2 | 1.97     |
| cpumanuf_dieadp  | kgSbeq/cm2  | 5.80E-07 |
| cpumanuf_diepe   | MJ/cm2      | 26.50    |
| cpumanuf_basegwp | kgCO2eq     | 9.14     |
| cpumanuf_baseadp | kgSbeq      | 2.04E-02 |
| cpumanuf_basepe  | MJ          | 156.00   |


## Usage impact

Both [power consumption](../usage/elec_conso.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

The CPU consumption profile is of the form : ```consumption_profile(workload) = a*ln(b+(workload*c))+d```

### Determining the parameters

#### From model range

If ```model_range``` is given or is completed from the ```cpu_name```, we use the averaged parameter for the specific model range.

|manufacturer|model_range  | a                 |b                   |c                 |d                  |
|------------|-------------|-------------------|--------------------|------------------|-------------------|
|Intel       |xeon platinum| 342.3624349628362 |0.034750819765533035|36.89522616719806 |-16.402219089443307|
|Intel       |xeon gold    | 71.13767381183924 |0.2280562153242743  |9.66939980437224  |6.266004455550223  |
|Intel       |xeon silver  | 41.55884200277906 |0.2805828410398358  |8.424085900547572 |4.764407035404158  |
|Intel       |xeon e5      | 97.83350026272564 |0.10296318761911205 |15.726228837967518|-1.8588498922070307|
|Intel       |xeon e3      | 342.3624349628362 |0.034750819765533035|36.89522616719806 |-16.402219089443307|
|Intel       |xeon e       | 55.65014194649273 |0.04666041377084888 |20.41458697644834 |4.243652609400892  |

By default, we use the consumption profile of **Intel Xeon Platinum**

![img_1.png](img_1.png)

#### Model adaptation from punctual measurement

In case punctual power measurement (load;power_consumption) are given by a user, we adapt the selected consumption profile to match the given point.

![img_2.png](img_2.png)

#### Model adaptation from from TDP

If the TDP is given we use the average power consumption per unit of TDP (given by TEADS) multiplied by the given TDP as power measurement and compute a model adaptation as describe above. 

| 0%   | 10%  | 50%   | 100%   |
|------|------|-------|--------|
| 0.12 | 0.32 | 0.75  | 1.02   |
*Average power consumption per unit of TDP*

