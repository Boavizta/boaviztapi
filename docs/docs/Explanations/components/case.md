# Case or Enclosure

## Characteristics

| Name       | Unit | Default value | Description                       | Example |
|------------|------|---------------|-----------------------------------|---------|
| units      | None | 1             | power supply quantity             | 2       |
| usage      | None | See Usage     | See usage                         | ..      |
| case_type  | None | rack          | Type of enclosure (blade or rack) | blade   |

## Manufacture impact

The manufacture impact of a **rack server**:

$$
\text{enclosure}_\text{manufacture}^\text{criteria} = \text{rack}_\text{manufacture}^\text{criteria}
$$

The manufacture impact of a **blade server**:

$$
\text{enclosure}_\text{manufacture}^\text{criteria} = \text{blade}_\text{manufacture}^\text{criteria}
+ \frac{\text{blade_enclosure}_\text{manufacture}^\text{criteria}}{16}
$$

With :

| Constant                                               | Unit    | Value     |
|--------------------------------------------------------|---------|-----------|
| $\text{rack}_\text{manufacture}^\text{gwp}$            | kgCO2eq | 150       |
| $\text{rack}_\text{manufacture}^\text{adp}$            | kgSbeq  | 2.02E-02  |
| $\text{rack}_\text{manufacture}^\text{pe}$             | MJ      | 2 200.00  |
| $\text{blade}_\text{manufacture}^\text{gwp}$           | kgCO2eq | 30.90     |
| $\text{blade}_\text{manufacture}^\text{adp}$           | kgSbeq  | 6.72E-04  |
| $\text{blade}_\text{manufacture}^\text{pe}$            | MJ      | 435.00    |
| $\text{blade_enclosure}_\text{manufacture}^\text{gwp}$ | kgCO2eq | 880.00    |
| $\text{blade_enclosure}_\text{manufacture}^\text{adp}$  | kgSbeq  | 4.32E-01  |
| $\text{blade_enclosure}_\text{manufacture}^\text{pe}$   | MJ      | 12 700.00 |

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented. In most cases, enclosure doesn't consume electricity.
