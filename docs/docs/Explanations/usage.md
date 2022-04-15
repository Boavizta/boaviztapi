# Usage impacts

Usage impacts are measured only at device level from usage configuration. Only GWP is implemented for now due to missing emissions factors for PE and ADP.

Usage impacts are measured by multiplying a **duration**, an **impact factor**, and an **electrical consumption** :

`impact = electrical_consumption*duration*impact_factor`

## Duration

Different from manufacture impacts, **usage impacts are measured for a specific time duration** given by the user.
The API handles three different time units :

| time unit |
| --------- |
| HOURS     |
| DAYS      |
| YEARS     |

In the general case, when duration is not given, the impact is measured for 1 year.

_Note : units are cumulative, if multiple units are used, they are summed._

### Example

```
HOURS = 1
DAYS = 1
YEARS =  1
```

will be converted in **8785** hours (`1+1*24+1*24*365`).

## Electrical impact factor

Impacts factor depends on the `usage_location` (country in a trigram format) of the device. `usage_location` can be defined by the user. By default, medium european mix is used.
Users can give their own impact factors in case it has been provided by their electricity provider.

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

If available, user should send the electrical consumption of his device in Watt/hour (`hours_electrical_consumption`).

### Retrieving electrical consumption

When users cannot send `hours_electrical_consumption`, the API retrieve it by multiplying the time and power per load for each load of a given segmentation.

#### Example - Dell r740

Taking the following load segmentation :

- 100%
- 50%
- 10%
- idle
- off

_note : any segmentation can be given_

##### Power ratio per load

Power per load is expressed as a ratio of `max_power`.

_max_power = 510_

| LOAD      | high (100%) | medium (50%) | low (10%) | idle   | off |
| --------- | ----------- | ------------ | --------- | ------ | --- |
| Power (W) | 1           | 0.7235       | 0.5118    | 0.3941 | 0   |

##### Time ratio per load

Time per load is expressed as a time ratio. It doesn't matter the duration nor the units since the ratio can be extrapolated to any duration.

| LOAD       | high (100%) | medium (50%) | low (10%) | idle | off |
| ---------- | ----------- | ------------ | --------- | ---- | --- |
| Time_ratio | 0.15        | 0.55         | 0.2       | 0.1  | 0   |

_note : the sum of time ratio per load must be 1._

##### Equation

`hours_electrical_consumption` is measured as follows :

```
hours_electrical_consumption = power(high) * time_ratio(high) + power(medium) * time_ratio(medium) + power(low) * time_ratio(low) + power(idle) * time_ratio(idle) + power(off) * time_ratio(off)
```

```
hours_electrical_consumption = (1*510) * 0.15 + (0.7235*510) * 0.55 + (0.5118*510) * 0.2 + (0.3941*510) * 0.1 + (0*510) * 0
                             = 351,74 W/hour
                             = 3081 kwh/year
```

##### Resource of the example

LCA of Dell r740 : [https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/Full_LCA_Dell_R740.pdf
](https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/Full_LCA_Dell_R740.pdf)

### Link with archetype

If you don't have the power per load or the time per load, it can be smart-completed with default values or completed from an [archetype](archetypes.md).
Both time or power can be completed.
