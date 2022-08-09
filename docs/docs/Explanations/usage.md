# Usage

Usage impacts are measured only at device level from usage configuration. 

Usage impacts are measured by multiplying a **duration**, an **impact factor**, and an **electrical consumption** :

```impact = electrical_consumption * duration * impact_factor```

## Duration

Usage impacts are measured for a specific time duration given by the user.
The API handles three different time units :

| time unit |
|-----------|
| HOURS     |
| DAYS      |
| YEARS     |

When duration is not given, the impact is measured for the default duration. Typically, 1 hour.
_Note : units are cumulative, if multiple units are used, they are summed._

### Example

```
HOURS = 1
DAYS = 1
YEARS =  1
```

will be converted in **8785** hours (`1+1*24+1*24*365`).


## Electrical impact factor

Impacts factor depends on the `usage_location`. `usage_location` can be defined by the user. By default, medium european mix is used.
Users can give their own impact factors in case it has been provided by their electricity provider.

`usage_location` are given in a trigram format. You can find the list of the available countries [here](countries.md).

### GWP - Global warming potential factor

_What_ : The amount of CO2eq. emitted per kwh of final energy production

_Source_ : 

* For Europe (2019) : https://www.sciencedirect.com/science/article/pii/S0306261921012149
* For the rest of the world (2011) : BASE IMPACT ADEME 

_Unit_ : kgCO2e/kWh

### PE - Primary energy factor

_What_ : The amount of primary energy consumed to produce 1 kWh of final energy (electricity in ICT use phase)

_Source_ : 

PE impact factor are not available in open access. 
We use the consumption of fossil resources per kwh (APDf/kwh) per country and extrapolate this consumption to renewable energy :

```PE/kwh = ADPf/kwh / (1-%RenewableEnergyInMix)```

* %RenewableEnergyInMix (2016) : 'https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production from IRENA
* ADPf (2011): BASE IMPACT ADEME

_Unit_ : MJ/kWh

### ADP

_What_ :  The amount of mineral and metalic resources consumed per kwh of final energy production

_Source_ : 

* ADP (2011) : BASE IMPACT ADEME 

_Unit_ : KgSbeq/kWh

## Electrical consumption

### Given

If available, user should send the electrical consumption of his components or devices in Watt/hour (`hours_electrical_consumption`).

### Modeled

Sometime user doesn't have access to the electrical consumption. 
If so, he can use the workload of the component or device as a proxy for the electrical consumption.
The API will use the consumption profile of the component or device.

### Consumption profile

A consumption profile is an equation which links a workload with an electrical consumption :
```consumption_profile(workload) = power_consumption```

To learn more about how we build consumption profile see consumption profile page.

Consumption profile can be given by the user or be completed.
The completion strategy of the consumption profile is specified for each device or component when implemented.

Consumption profile is implemented for :

* [CPU](components/cpu.md)
* [RAM](components/ram.md)
* [SERVER](devices/server.md)
* [CLOUD INSTANCES](devices/cloud.md)

### Workload

Workload is given by the user as a ratio of the maximum workload.

An average workloads can be given. A workload of 0.1 will mean : *"I used my component or device in average at 10% of workload"*

A Workload can be given as a dictionary which links a workload and duration ratio at this workload.
The following 

```json
{
"0.1": 0.5,
"0.5": 0.2,
"1": 0.3 
}
```

will mean : *"I used my component or device 50% of the time at 10% of its maximum of workload, 20%  of the time at 50% of its maximum of workload and 30% of the time at its maximum workload (100%)"*

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

##### Resource of the example

LCA of Dell r740 : [https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/Full_LCA_Dell_R740.pdf
](https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/Full_LCA_Dell_R740.pdf)






