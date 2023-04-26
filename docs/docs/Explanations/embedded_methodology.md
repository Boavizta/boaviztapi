# EMBEDDED IMPACTS METHODOLOGY

!!!info
    Embedded impacts include the impacts occurring during raw material extraction,
    manufacture, transport and end of life phases.

## Components impacts

### Variable components impacts

The impacts of variable components are assessed from the component characteristics.

* [CPU](components/cpu.md)
* [RAM](components/ram.md)
* [DISK (SSD)](components/ssd.md)

!!!warning
    For now, transport and end of life are not taken into account.

### Fixed components impacts

The impacts of fixed components are set by default

* [DISK (HDD)](components/hdd.md)
* [MOTHERBOARD](components/motherboard.md)
* [POWER SUPPLY](components/power_supply.md)
* [ASSEMBLY](components/assembly.md)

!!!warning
    For now, transport and end of life are not taken into account.

## Device impacts

The data and methods are specified for each device in their dedicated page.

* [Server](devices/server.md)
* [Cloud instances](devices/cloud.md)
* [End user devices](devices/end_user_devices.md)

Two strategies exist

### 1. Bottom-up approach

Embedded impacts are assessed at component level and aggregated at device level with a bottom-up approach. 

!!!warning
    In this case, transport and end of life are not taken into account for now.

### 2. Fix impacts factors

If component impacts cannot be assessed, we use non-specific impacts factors at device level.

!!!warning
    In this case, all the life cycle is taken into account including transport and end of life.

## Allocation

Embedded impacts can be reported with several allocation strategies.

### Hover the lifecycle - ```Allocation: TOTAL```

The total embedded impacts are reported independently of the usage.

```manufacture_impacts = total_impact```

### Hover a specific duration - ```Allocation: LINEAR```

The embedded impacts is linearly distributed hover the life duration of the devices.
The impacts are queried hover the usage duration.

```manufacture_impacts = total_impacts * (usage_duration/life_duration)```

## Resources

[Boavizta server impacts measurement methodology](https://boavizta.org/blog/numerique-et-environnement-comment-evaluer-l-empreinte-de-la-fabrication-d-un-serveur-au-dela-des-emissions-de-gaz-a-effet-de-se?token=2112aecb183b1b5d27e137abc61e0f0d39fabf99)
