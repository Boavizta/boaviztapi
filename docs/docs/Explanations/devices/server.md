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

<h6>server<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>manuf<sub><em>criteria</em></sub></sub> + ram<sub>manuf<sub><em>criteria</em></sub></sub> + ssd<sub>manuf<sub><em>criteria</em></sub></sub>+ hdd<sub>manuf<sub><em>criteria</em></sub></sub> + motherboard<sub>manuf<sub><em>criteria</em></sub></sub> + psu<sub>manuf<sub><em>criteria</em></sub></sub> + enclosure<sub>manuf<sub><em>criteria</em></sub></sub> + assembly<sub>manuf<sub><em>criteria</em></sub></sub></h6>

## Usage impact

Both [power consumption](../usage/elec_conso.md) and [consumption profile](../consumption_profile.md) are implemented.

## Consumption profile

A server consumption profile is of the form : 

```consumption_profile(workload) = (consumption_profile_cpu(workload)+consumption_profile_ram(workload))(1+other_consumption_ratio)```

```consumption_profile_cpu(workload)``` and ```consumption_profile_ram(workload)``` depend on the technical characteristics of the RAM and CPU.
```Other_consumption_ratio``` is used to account for the electrical consumption of the other components (other than RAM and CPU). 
It is arbitrary set to 0.3 and can modify by users.