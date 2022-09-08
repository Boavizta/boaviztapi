# CPU

## Characteristics

| Name              | Unit | Default value | Description                                   | Example            |
|-------------------|------|---------------|-----------------------------------------------|--------------------|
| units             | None | 1             | CPU quantity                                  | 2                  |
| usage             | None | See Usage     | See usage                                     | ..                 |
| core_units        | None | 24            | Number of core on one CPU                     | 12                 |
| die_size          | mm2  | None          | Size of the die                               | 2900               |
| manufacturer      | None | Intel         | Name of the CPU manufacturer                  | AMD                |
| die_size_per_core | mm2  | 0.245         | Size of the die divided by the number of core | 0.245              |
| model_range       | None | Xeon Platinum | Name of the cpu range or brand                | i7                 |
| family            | None | Skylake       | Name of the architectural family (Generation) | Naple              |
| name              | None | None          | Complete commercial name of the CPU           | Intel Core i7-1065 |


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

if they can not be found, default data are used.

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

The consumption profile depends on the cpu model range. By default we use the consumption profile of **Xeon Platinium**.