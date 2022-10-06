# RAM

## Characteristics

| Name             | Unit   | Default value | Description                           | Example |
|------------------|--------|---------------|---------------------------------------|---------|
| units            | None   | 1             | RAM strip quantity                    | 2       |
| usage            | None   | See Usage     | See usage                             | ..      |
| capacity         | Go     | 32            | Capacity of a ram strip               | 12      |
| density          | cm2/Go | 0.625         | Size of the die per Go of a ram strip | 1.25    |
| process          | nm     | None          | Engraving process (Architecture)      | 25      |
| manufacturer     | None   | None          | Name of the ram manufacturer          | Samsung |
| model            | None   | None          | ..                                    | ..      |


## Complete

**The following variables can be [completed](../complete.md)**

### density

if ```process``` or/and ```manufacturer``` are given, ```density``` can be retrieved from a fuzzy matching on our ram repository.
If several ram matches the given ```process``` or/and ```manufacturer``` the maximizing value is given (in terms of impacts).

## Manufacture impact

For one RAM bank the manufacture impact is:

$$
\text{RAM}_\text{manufacture}^\text{criteria} = (\text{RAM}_{\text{capacity}} / \text{RAM}_{\text{density}}) * \text{RAM}_\text{manufacture_die}^\text{criteria} + \text{RAM}_\text{manufacture_base}^\text{criteria}
$$

with:

| Constant                                        | Units       | Value      |
|-------------------------------------------------|-------------|------------|
| $\text{RAM}_\text{manufacture_die}^\text{gwp}$  | kgCO2eq/cm2 | 2.20       |
| $\text{RAM}_\text{manufacture_die}^\text{adp}$  | kgSbeq/cm2  | 6.30E-05   |
| $\text{RAM}_\text{manufacture_die}^\text{pe}$   | MJ/cm2      | 27.30      |
| $\text{RAM}_\text{manufacture_base}^\text{gwp}$ | kgCO2eq     | 5.22       |
| $\text{RAM}_\text{manufacture_base}^\text{adp}$ | kgSbeq      | 1.69E-03   |
| $\text{RAM}_\text{manufacture_base}^\text{pe}$  | MJ          | 74.00      |

_Note: If there are more than 1 RAM bank we multiply $\text{RAM}_\text{manufacture}^\text{criteria}$ by the number of RAM bank given in `units`._


## Usage impact

Both [power consumption](../usage/elec_conso.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

The RAM consumption profile is of the form : ```consumption_profile(workload) = a * capacity```

As a first approximation, we use a uniform consumption profile since the stress test data used show a rather uniform
consumption. Consequently, the workload won't be used.

![cp_ram.png](cp_ram.png)

New stress test data specifically on RAM calls should be conducted to specify this consumption profile.

### Determining the parameters

To determine ```a``` we averaged the electrical consumption of RAM per GB. With the process we came up with ```a=0.284```

Capacity is either given by the user or the default value is used.

```consumption_profile(workload) = 0.284 * capacity```