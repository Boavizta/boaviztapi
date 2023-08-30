# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of a CPU. See the detailed documentation for the other components.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws/all_instances' | jq`)_

## Get the impacts from cpu name

In this query, we use the cpu name to evaluate its impact.

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

This query returns :

- The impacts for the default criteria (gwp, pe, adp) since no impact is specified
- The total embedded impacts of the CPU
- The usage impacts of the CPU during the life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

Result :

```json
{
  "gwp": {
    "embedded": {
      "value": 21.927,
      "significant_figures": 5,
      "min": 10.6,
      "max": 44.149,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 944.95,
      "significant_figures": 5,
      "min": 57.195,
      "max": 2814
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "embedded": {
      "value": 0.020404,
      "significant_figures": 5,
      "min": 0.0204,
      "max": 0.02041,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.00015973,
      "significant_figures": 5,
      "min": 3.2924e-05,
      "max": 0.00066041
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "embedded": {
      "value": 328.01,
      "significant_figures": 5,
      "min": 175.64,
      "max": 626.93,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 32012,
      "significant_figures": 5,
      "min": 32.327,
      "max": 1164200
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
}
```

## Get the values used to assess the impacts of the cpu

This is the same query as before. However, you add the `verbose=true` flag to get the value of the attributes used for the calculation.

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=true&criteria=gwp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

Result :

* This query returns will only compute the gwp impact since we add the `criteria=gwp` flag.
* You can see that the API has completed the needed value from the cpu name. We parse and fuzzymatch the cpu ```name``` with our dataset of cpu to identify ```tdp```, ```cores_unit```, ```family```...
* The ```die_size_per_core``` is completed from the cpu family.
* The usage impact has been assessed using a default level of workload of 50% with the consumption profile of a xeon gold (completed from cpu ```name```).

```json
{
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 21.927,
        "significant_figures": 5,
        "min": 10.6,
        "max": 44.149,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 944.95,
        "significant_figures": 5,
        "min": 57.195,
        "max": 2814
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    }
  },
  "verbose": {
    "impacts": {
      "gwp": {
        "embedded": {
          "value": 21.927,
          "significant_figures": 5,
          "min": 10.6,
          "max": 44.149,
          "warnings": [
            "End of life is not included in the calculation"
          ]
        },
        "use": {
          "value": 944.95,
          "significant_figures": 5,
          "min": 57.195,
          "max": 2814
        },
        "unit": "kgCO2eq",
        "description": "Total climate change"
      }
    },
    "units": {
      "value": 1,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 1
    },
    "core_units": {
      "value": 24,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 64
    },
    "die_size_per_core": {
      "value": 25,
      "status": "COMPLETED",
      "unit": "mm2",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)#Extreme_Core_Count_.28XCC.29",
      "min": 25,
      "max": 27
    },
    "model_range": {
      "value": "Xeon Gold",
      "status": "COMPLETED",
      "source": "Completed from name name based on https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data.",
      "min": "Xeon Gold",
      "max": "Xeon Gold"
    },
    "manufacturer": {
      "value": "Intel",
      "status": "COMPLETED",
      "source": "Completed from name name based on https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data.",
      "min": "Intel",
      "max": "Intel"
    },
    "family": {
      "value": "skylake",
      "status": "CHANGED",
      "source": "Completed from name name based on https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data."
    },
    "name": {
      "value": "Intel Xeon Gold 6134",
      "status": "COMPLETED",
      "source": "fuzzy match",
      "min": "Intel Xeon Gold 6134",
      "max": "Intel Xeon Gold 6134"
    },
    "duration": {
      "value": 26280,
      "unit": "hours"
    },
    "avg_power": {
      "value": 94.624,
      "status": "COMPLETED",
      "unit": "W",
      "min": 94.624,
      "max": 94.624
    },
    "time_workload": {
      "value": 50,
      "status": "ARCHETYPE",
      "unit": "%",
      "min": 0,
      "max": 100
    },
    "usage_location": {
      "value": "EEE",
      "status": "DEFAULT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    },
    "use_time_ratio": {
      "value": 1,
      "status": "ARCHETYPE",
      "unit": "/1",
      "min": 1,
      "max": 1
    },
    "hours_life_time": {
      "value": 26280,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 26280,
      "max": 26280
    },
    "params": {
      "value": {
        "a": 35.5688,
        "b": 0.2438,
        "c": 9.6694,
        "d": -0.6087
      },
      "status": "COMPLETED",
      "source": "From CPU model range"
    },
    "gwp_factor": {
      "value": 0.38,
      "status": "DEFAULT",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
      "min": 0.023,
      "max": 1.13161
    }
  }
}
```

## Get the impacts from custom cpu characteristics

In this query, we give some characteristics to describe the CPU. 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=true&criteria=gwp&criteria=adp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
 -d '{
      "core_units": 24,
      "family": "Skylake"
      }'
```
Result :

* This query returns will compute the gwp and adp impacts since we add the `criteria=gwp&criteria=adp` flags.
* Since only lowercase is used, the API will correct Skylake to skylake (CHANGED) and complete the missing attributes from the given attributes (COMPLETED) or by default ones (ARCEHTYPE).

```json
{
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 21.927,
        "significant_figures": 5,
        "min": 21.927,
        "max": 22.873,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 1819.8,
        "significant_figures": 5,
        "min": 110.15,
        "max": 5419.3
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "embedded": {
        "value": 0.020404,
        "significant_figures": 5,
        "min": 0.020404,
        "max": 0.020404,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 0.00030761,
        "significant_figures": 5,
        "min": 6.3406e-05,
        "max": 0.0012718
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    }
  },
  "verbose": {
    "impacts": {
      "gwp": {
        "embedded": {
          "value": 21.927,
          "significant_figures": 5,
          "min": 21.927,
          "max": 22.873,
          "warnings": [
            "End of life is not included in the calculation"
          ]
        },
        "use": {
          "value": 1819.8,
          "significant_figures": 5,
          "min": 110.15,
          "max": 5419.3
        },
        "unit": "kgCO2eq",
        "description": "Total climate change"
      },
      "adp": {
        "embedded": {
          "value": 0.020404,
          "significant_figures": 5,
          "min": 0.020404,
          "max": 0.020404,
          "warnings": [
            "End of life is not included in the calculation"
          ]
        },
        "use": {
          "value": 0.00030761,
          "significant_figures": 5,
          "min": 6.3406e-05,
          "max": 0.0012718
        },
        "unit": "kgSbeq",
        "description": "Use of minerals and fossil ressources"
      }
    },
    "units": {
      "value": 1,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 1
    },
    "core_units": {
      "value": 24,
      "status": "INPUT"
    },
    "die_size_per_core": {
      "value": 25,
      "status": "COMPLETED",
      "unit": "mm2",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)#Extreme_Core_Count_.28XCC.29",
      "min": 25,
      "max": 27
    },
    "family": {
      "value": "skylake",
      "status": "CHANGED"
    },
    "duration": {
      "value": 26280,
      "unit": "hours"
    },
    "avg_power": {
      "value": 182.23,
      "status": "COMPLETED",
      "unit": "W",
      "min": 182.23,
      "max": 182.23
    },
    "time_workload": {
      "value": 50,
      "status": "ARCHETYPE",
      "unit": "%",
      "min": 0,
      "max": 100
    },
    "usage_location": {
      "value": "EEE",
      "status": "DEFAULT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    },
    "use_time_ratio": {
      "value": 1,
      "status": "ARCHETYPE",
      "unit": "/1",
      "min": 1,
      "max": 1
    },
    "hours_life_time": {
      "value": 26280,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 26280,
      "max": 26280
    },
    "params": {
      "value": {
        "a": 171.2,
        "b": 0.0354,
        "c": 36.89,
        "d": -10.13
      },
      "status": "ARCHETYPE"
    },
    "gwp_factor": {
      "value": 0.38,
      "status": "DEFAULT",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
      "min": 0.023,
      "max": 1.13161
    },
    "adp_factor": {
      "value": 6.42317e-08,
      "status": "DEFAULT",
      "unit": "kg Sbeq/kWh",
      "source": "ADEME Base IMPACTS ®",
      "min": 1.324e-08,
      "max": 2.65575e-07
    }
  }
}
```

## Get the impacts from custom cpu usage using an electrical consumption

In this query we set a custom usage to an ```intel xeon gold 6134```. The average electrical consumption is given.

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false&criteria=gwp&duration=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134",
  "usage":{
      "usage_location": "FRA",
      "avg_power": 120
  }}'
```

Result : 

* The API will use an electrical consumption of 120 Watt/hours for 2 hours (since duration is set at 2)
* Usage impacts will be assessed for the French electrical mix impacts 
* Embedded impacts will be allocated on 2 hours


```json
{
  "gwp": {
    "embedded": {
      "value": 0.0016687,
      "significant_figures": 5,
      "min": 0.00080668,
      "max": 0.0033599,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.02352,
      "significant_figures": 5,
      "min": 0.02352,
      "max": 0.02352
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  }
}
```


## Get the impacts from custom cpu usage using a workload

In this query we set a custom usage to an ```intel xeon gold 6134``` with a TDP of 130 Watt. The average electrical consumption is retrieved.

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false&criteria=gwp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134",
  "tdp": 130,
  "usage":{
      "hours_use_time": 2,
      "usage_location": "FRA",
      "time_workload": 30
  }}'
```

Result : 

* The API will use the ```xeon gold``` consumption profile adapted for a TDP of 130 Watt with a level of workload of 30% for 2 hours to retrieve the electrical consumption of the CPU.

```json
{
  "gwp": {
    "embedded": {
      "value": 21.927,
      "significant_figures": 5,
      "min": 10.6,
      "max": 44.149,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 205.09,
      "significant_figures": 5,
      "min": 205.09,
      "max": 205.09
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  }
}
```

For further information see : [The explanation page on cpu](../Explanations/components/cpu.md)