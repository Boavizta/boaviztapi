# Power supply

## Characteristics

| Name               | Unit | Default value | Description                 | Example |
|--------------------|------|---------------|-----------------------------|---------|
| units              | None | 1             | power supply quantity       | 2       |
| usage              | None | See Usage     | See usage                   | ..      |
| unit_weight        | kg   | 2.99          | weight of the power supply  | 5       |

## Manufacture impact

For one power supply the manufacture impact is:

$$
\text{power_supply}_\text{manufacture}^\text{criteria} = \text{power_supply}_\text{unit_weight} * \text{power_supply}_
\text{manufacture_weight}^\text{criteria}
$$

with :

| Constant                                                   | Unit       | Value    |
|------------------------------------------------------------|------------|----------|
| $\text{power_supply}_\text{manufacture_weight}^\text{gwp}$ | kgCO2eq/kg | 24.30    |
| $\text{power_supply}_\text{manufacture_weight}^\text{adp}$ | kgSbeq/kg  | 8.30E-03 |
| $\text{power_supply}_\text{manufacture_weight}^\text{pe}$  | MJ/kg      | 352.00   |

_Note: If there are more than 1 power we multiply $\text{power_supply}_\text{manufacture}^\text{criteria}$ by the number
of power supply given in `units`._

## Usage impact

Only [power consumption](../usage/elec_conso.md) is implemented.
This shouldn't be used in most cases since the electricity consume by a power supply is consume on behalf of other
components.