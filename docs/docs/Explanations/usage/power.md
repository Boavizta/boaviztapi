# Power

## Given

If available, user should send the power of his asset in Watt.
Since the power will be extrapolated on the all duration, the power given should be the average power of the asset over the given duration.

!!!info
    The power can be given in usage object with the attribute `avg_power` in Watt.

## Completed from the [archetype](../archetypes.md).

If available, the API will complete the missing power by the one taken from the archetype of the asset.

## Modeling

Sometime user doesn't have access to the power of their asset, and we don't want to use a default value taken from an archetype.

If so, the API can use the percentage of asset' resource usage as a proxy for the power. We refer to this percentage as a workload of the asset.
The API is able to convert a workload into a power consumption with consumption profiles.

To learn more about how we build consumption profile see consumption [profile page](../consumption_profile.md).

### Using consumption profile

Workload are given by the user as a percentage of the maximum workload.

An average workloads can be given. A workload of 10% will mean : *"I used my asset in average at 10% of its maximum workload"*

A workload can also be given as a dictionary to specify the percentage of time spent at each desired workload level.
The following 

```json
[
    {
        "load_percentage": 10,
        "time_percentage": 50
    },
    {
        "load_percentage": 50,
        "time_percentage": 20
    },
    {
        "load_percentage": 100,
        "time_percentage": 30
    }
]
```

This translates into using an asset:

- 50% of the time at 10% ot its maximum workload,
- 20% of the time at 50% of its maximum workload,
- 30% of the time at the maximum workload

### Example for a CPU

Taking the following load segmentation :

- 100%
- 50%
- 10%
- 0% (IDLE)
- off

With the following time repartition

| load_percentage | high (100%) | medium (50%) | low (10%) | idle | off |
|-----------------|-------------|--------------|-----------|------|-----|
| time_percentage | 15%         | 55%          | 10%       | 20%  | 0%  |

_note : the sum of time ratio per load must be 100._

With the following consumption profile : 

```consumption_profile(workload) = 55.65 * ln(0.046 * (workload + 20.41)) + 4.24```

Power consumptions : 

| load_percentage | 100% | 50%  | 10%   | idle | off   |
|-----------------|------|------|-------|------|-------|
| Power (W)       | 100  | 70   | 24    | 2    | 0     |

`avg_power` is measured as follows :

```
avg_power = power(100%) * time_ratio(100%) + power(50%) * time_ratio(50%) + power(10%) * time_ratio(10%) + power(idle) * time_ratio(idle) + power(off) * time_ratio(off)
```

```
avg_power = 260 * 0.15 + 182 * 0.55 + 77 * 0.1 + 36 * 0.2 + 0 * 0
                             = 39 + 100.1 + 7,7 + 7,2 + 0
                             = 154 W/hour
                             = 1349 kwh/year
```

**Result : ** 154 W/hour

