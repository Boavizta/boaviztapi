# Electrical consumption

## Given

If available, user should send the electrical consumption of his components or devices in Watt/hour (`hours_electrical_consumption`).
Since the power will be extrapolated on the all duration, the power given should be The average power of the device or component over the given duration.


## Modeled

Sometime user doesn't have access to the electrical consumption of their component or device.
If so, he can use the percentage of component' or device' resource usage as a proxy for the electrical consumption. We refer the percentage as the workload of the component or device.
The API is able to convert a workload into a power consumption with consumption profiles.

To learn more about how we build consumption profile see consumption [profile page](../consumption_profile.md).

### Using consumption profile

Workload is given by the user as a percentage of the maximum workload.

An average workloads can be given. A workload of 10% will mean : *"I used my component or device in average at 10% of workload"*

A Workload can be given as a dictionary which links a workload and duration ratio at this workload.
The following 

```json
[{
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

will mean : *"I used my component or device at 50% of the time at 10% of its maximum of workload, 20%  of the time at 50% of its maximum of workload and 30% of the time at its maximum workload (100%)"*

### Example

Taking the following load segmentation :

- 100%
- 50%
- 10%
- 0% (IDLE)
- off

With the following time repartition

| LOAD       | high (100%) | medium (50%) | idle | low (10%) | off  |
| ---------- | ----------- | ------------ | ---- | --------- |------|
| Time_ratio | 0.15        | 0.55         | 0.1  | 0.2       | 0    |

_note : the sum of time ratio per load must be 1._

With the following consumption profile : 

```consumption_profile(workload) = a * ln(b * (workload + c)) + d```

Power consumptions : 

| LOAD      | 100% | 50% | 10% | idle | off |
| --------- |------|-----|-----|------|-----|
| Power (W) |      |     |     |      | 0   |

`hours_electrical_consumption` is measured as follows :

```
hours_electrical_consumption = power(100%) * time_ratio(100%) + power(50% ) * time_ratio(50%) + power(10%) * time_ratio(10%) + power(idle) * time_ratio(idle) + power(off) * time_ratio(off)
```

```
hours_electrical_consumption = (1*510) * 0.15 + (0.7235*510) * 0.55 + (0.5118*510) * 0.2 + (0.3941*510) * 0.1 + (0*510) * 0
                             = 351,74 W/hour
                             = 3081 kwh/year
```



