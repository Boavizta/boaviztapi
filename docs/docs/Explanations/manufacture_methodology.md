# MANUFACTURE METHODOLOGY

Manufacture impacts are measured at components and device level with a bottom-up approach.

## Allocation

Manufacture impacts can be reported with several allocation strategies.

### Hover the lifecycle - ```Allocation: TOTAL```

The total manufacturing impacts are reported independently of the usage.

```manufacture_impact = total_impact```

### Hover a specific duration - ```Allocation: LINEAR```

The manufacturing impacts is linearly distributed hover the life duration of the devices.
The impacts are reported hover the usage duration.

```manufacture_impact = total_impact * (usage_duration/life_duration)```


## Variable components impacts

The impact of variable components are evaluated from the components characteristics.

* [CPU](components/cpu.md)
* [RAM](components/ram.md)
* [DISK (SSD)](components/ssd.md)


## Fixed components impacts

The impact of fixed component are set by default

* [DISK (HDD)](components/hdd.md)
* [MOTHERBOARD](components/motherboard.md)
* [POWER SUPPLY](components/power_supply.md)
* [ASSEMBLY](components/assembly.md)


## Device impacts

Device impacts is evaluated from the sum of the impacts of its components. Other treatments can be applied depending on the device.

## Resources

[Boavizta server impact measurement methodology](https://boavizta.cmakers.io/blog/numerique-et-environnement-comment-evaluer-l-empreinte-de-la-fabrication-d-un-serveur-au-dela-des-emissions-de-gaz-a-effet-de-se?token=2112aecb183b1b5d27e137abc61e0f0d39fabf99)

