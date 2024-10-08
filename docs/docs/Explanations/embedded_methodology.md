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
* [Functional blocks (IoT)](components/functional_blocks.md)

!!!warning
    For now end of life is not taken into account.

### Fixed components impacts

The impacts of fixed components are set by default

* [DISK (HDD)](components/hdd.md)
* [MOTHERBOARD](components/motherboard.md)
* [POWER SUPPLY](components/power_supply.md)
* [ASSEMBLY](components/assembly.md)

!!!warning
    For now end of life is not taken into account.

## Device & services impacts

The data and methods are specified for each device or service in their dedicated page.

* [Server](devices/server.md)
* [Cloud instances](services/cloud.md)
* [End user devices](devices/terminals_&_peripherals.md)
* [IoT devices](devices/iot_devices.md)

Two strategies exist

### 1. Bottom-up approach

Embedded impacts are assessed at component level and aggregated at device level with a bottom-up approach. 

!!!warning
    In this case, end of life is not taken into account for now.

### 2. Fix impacts factors

If component impacts cannot be assessed, we use non-specific impacts factors at device level.

!!!warning
    In this case, all the life cycle is taken into account including end of life.

## Allocation

Embedded impacts can be reported with several allocation strategies.

### Over the lifecycle 

When no specific duration is given, the total embedded impacts of the asset are given.

```embedded_impacts = total_impact```

### Over a specific duration

When a duration is given as a query parameter, we allocate the embedded impacts linearly on this duration.

```embedded_impacts = total_impacts * (duration/life_duration)```

## Resources

[Boavizta server impacts measurement methodology](https://boavizta.org/en/blog/empreinte-de-la-fabrication-d-un-serveur)
