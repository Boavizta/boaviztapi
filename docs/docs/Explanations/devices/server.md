# Server

## Characteristics

| Name         | Unit | Default value                                                 | Description    | Example |
|--------------|------|---------------------------------------------------------------|----------------|---------|
| usage        | None | See [server usage](../usage/usage.md)                         |                | ..      |
| cpu          | None | See [cpu](../components/cpu.md)                               |                | ..      |
| ram          | None | See [ram](../components/ram.md)                               |                | ..      |
| disk         | None | See [ssd](../components/ssd.md) & [hdd](../components/hdd.md) | SSD or HDD     | ..      |
| motherboard  | None | See [motherboad](../components/motherboard.md)                 |                | ..      |
| power_supply | None | See [power_supply](../components/power_supply.md)             |                | ..      |
| assembly     | None | See [assembly](../components/assembly.md)                     | Assembly phase | ..      |
| case         | None | See [case](../components/case.md)                             | Enclosure      | ..      |

## Complete

The following component are [completed](../complete.md) with the default characteristics if not given by the user:

* 2  [CPU](../components/cpu.md)
* 24 [RAM](../components/ram.md)
* 1  [SSD](../components/ssd.md)
* 2  [power supplies](../components/power_supply.md)
* 1  [case](../components/case.md)

## Manufacture impact

$$
\begin{equation}
\begin{aligned}
\text{server}_\text{manufacture}^\text{criteria} & = \sum_{\set{\text{components}}}{\text{component}_
\text{manufacture}^\text{criteria}} \\ \\
& = \text{cpu_units} * \text{CPU}_{manufacture}^{criteria} \\
& \quad + \ \text{ram_units} * \text{RAM}_{manufacture}^{criteria} \\
& \quad + \ \text{ssd_units} * \text{SSD}_{manufacture}^{criteria} \\
& \quad + \ \text{hdd_units} * \text{HDD}_{manufacture}^{criteria} \\
& \quad + \ \text{motherboard}_{manufacture}^{criteria} \\
& \quad + \ \text{power_supply_units} * \text{power_supply}_{manufacture}^{criteria} \\
& \quad + \ \text{assembly}_{manufacture}^{criteria} \\
& \quad + \ \text{enclosure}_{manufacture}^{criteria}
\end{aligned}
\end{equation}
$$

## Usage impact

Both [power consumption](../usage/elec_conso.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

A server consumption profile is of the form :

$$
\text{CP}_{\text{component}} = \text{consumption_profile}_{\text{component}}
$$

$$
\text{CP}(\text{workload}) = (\text{CP}_{\text{CPU}}(\text{workload})
+ \text{CP}_{\text{RAM}}(\text{workload}))
* (1 + \text{other_consumption_ratio})
$$

$\text{CP}_{\text{CPU}}(\text{workload})$ and $\text{CP}_{\text{RAM}}(\text{workload})$ depend on the technical
characteristics of the RAM and CPU.
```other_consumption_ratio``` is used to account for the electrical consumption of the other components (other than RAM
and CPU).
It is arbitrary set to 0.3 and can modify by users.