# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of a CPU. See the detailed documentation for the other components.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws/all_instances' | jq`)_

## Get the impacts from cpu name

In this query, we use the cpu name to evaluate its impact.

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

This query returns :

- The total embedded impacts (for gwp, pe, adp) of the CPU
- The usage impacts (for gwp, pe, adp) of the CPU for one year (default)
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

Result :

```json
{
  "gwp": {
    "other": {
      "value": 17.5,
      "significant_figures": 3,
      "min": 11.2,
      "max": 26.2
    },
    "use": {
      "value": 320,
      "significant_figures": 2,
      "min": 19,
      "max": 750
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "other": {
      "value": 0.02,
      "significant_figures": 2,
      "min": 0.02,
      "max": 0.02
    },
    "use": {
      "value": 5.35e-05,
      "significant_figures": 3,
      "min": 1.1e-05,
      "max": 0.000221
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "other": {
      "value": 269,
      "significant_figures": 3,
      "min": 184,
      "max": 385
    },
    "use": {
      "value": 10720,
      "significant_figures": 4,
      "min": 10.83,
      "max": 390000
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
  '{{ endpoint }}/v1/component/cpu?verbose=true&allocation=TOTAL&criteria=gwp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

This query returns will only compute the gwp impact since we add the `criteria=gwp` flag.

Result :

You can see that the API has completed the needed value from the cpu name. We parse and fuzzymatch the cpu ```name``` with our dataset of cpu to identify ```tdp```, ```cores_unit```, ```family```...
The ```die_size_per_core``` is completed from the cpu family.

The usage impact has been assessed using a default level of workload of 50% with the consumption profile of a xeon gold (completed from cpu ```name```).

```json
{
  "impacts": {
    "gwp": {
      "other": {
        "value": 17.5,
        "significant_figures": 3,
        "min": 11.2,
        "max": 26.2
      },
      "use": {
        "value": 320,
        "significant_figures": 2,
        "min": 19,
        "max": 750
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    }
  },
  "verbose": {
    "impacts": {
      "gwp": {
        "other": {
          "value": 17.5,
          "significant_figures": 3,
          "min": 11.2,
          "max": 26.2
        },
        "use": {
          "value": 320,
          "significant_figures": 2,
          "min": 19,
          "max": 750
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
      "value": 8,
      "status": "COMPLETED",
      "source": "from name",
      "min": 8,
      "max": 8
    },
    "die_size_per_core": {
      "value": 0.47078947368421054,
      "status": "COMPLETED",
      "unit": "mm2",
      "source": "Average for skylake",
      "min": 0.07,
      "max": 1.02
    },
    "family": {
      "value": "skylake",
      "status": "COMPLETED",
      "source": "from name",
      "min": "skylake",
      "max": "skylake"
    },
    "name": {
      "value": "Intel Xeon Gold 6134",
      "status": "COMPLETED",
      "source": "fuzzy match",
      "min": "Intel Xeon Gold 6134",
      "max": "Intel Xeon Gold 6134"
    },
    "tdp": {
      "value": 130,
      "status": "COMPLETED",
      "unit": "W",
      "source": "from name",
      "min": 130,
      "max": 130
    },
    "hours_electrical_consumption": {
      "value": 95.095,
      "status": "COMPLETED",
      "unit": "W",
      "min": 95.095,
      "max": 95.095
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
    "use_time": {
      "value": 8760,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 8760,
      "max": 8760
    },
    "workloads": {
      "value": [
        {
          "load_percentage": 0,
          "power_watt": 15.6
        },
        {
          "load_percentage": 10,
          "power_watt": 41.6
        },
        {
          "load_percentage": 50,
          "power_watt": 97.5
        },
        {
          "load_percentage": 100,
          "power_watt": 132.6
        }
      ],
      "status": "COMPLETED",
      "unit": "workload_rate:W"
    },
    "params": {
      "value": {
        "a": 85.60000000000328,
        "b": 0.0405162074578643,
        "c": 33.86103837773685,
        "d": -9.60289959210695
      },
      "status": "COMPLETED",
      "source": "From TDP"
    },
    "gwp_factor": {
      "value": 0.38,
      "status": "DEFAULT",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries",
      "min": 0.023,
      "max": 0.9
    }
  }
}
```

## Get the impacts from custom cpu characteristics

In this query, we give some characteristics to describe the CPU. 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=true&allocation=TOTAL&criteria=gwp&criteria=adp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
 -d '{
      "core_units": 24,
      "family": "Skylake"
      }'
```

This query returns will compute the gwp and adp impacts since we add the `criteria=gwp&criteria=adp` flags.

Result :

Since only lowercase is used, the API will correct Skylake to skylake (CHANGED) and complete the missing attributes from the given attributes (COMPLETED) or by default ones (ARCEHTYPE).

```json
{
  "impacts": {
    "gwp": {
      "other": {
        "value": 22,
        "significant_figures": 2,
        "min": 22,
        "max": 23
      },
      "use": {
        "value": 610,
        "significant_figures": 2,
        "min": 37,
        "max": 1400
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "other": {
        "value": 0.02,
        "significant_figures": 2,
        "min": 0.02,
        "max": 0.02
      },
      "use": {
        "value": 0.000102,
        "significant_figures": 3,
        "min": 2.11e-05,
        "max": 0.000424
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    }
  },
  "verbose": {
    "impacts": {
      "gwp": {
        "other": {
          "value": 22,
          "significant_figures": 2,
          "min": 22,
          "max": 23
        },
        "use": {
          "value": 610,
          "significant_figures": 2,
          "min": 37,
          "max": 1400
        },
        "unit": "kgCO2eq",
        "description": "Total climate change"
      },
      "adp": {
        "other": {
          "value": 0.02,
          "significant_figures": 2,
          "min": 0.02,
          "max": 0.02
        },
        "use": {
          "value": 0.000102,
          "significant_figures": 3,
          "min": 2.11e-05,
          "max": 0.000424
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
      "value": 0.25,
      "status": "COMPLETED",
      "unit": "mm2",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)#Extreme_Core_Count_.28XCC.29",
      "min": 0.25,
      "max": 0.27
    },
    "family": {
      "value": "skylake",
      "status": "CHANGED"
    },
    "hours_electrical_consumption": {
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
    "use_time": {
      "value": 8760,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 8760,
      "max": 8760
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
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries",
      "min": 0.023,
      "max": 0.9
    },
    "adp_factor": {
      "value": 6.42e-08,
      "status": "DEFAULT",
      "unit": "kg Sbeq/kWh",
      "source": "ADEME BASE IMPACT",
      "min": 1.32e-08,
      "max": 2.656e-07
    }
  }
}
```

## Get the impacts from custom cpu usage using an electrical consumption

In this query we set a custom usage to an ```intel xeon gold 6134```. The average electrical consumption is given.

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false&allocation=TOTAL&criteria=gwp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134",
  "usage":{
      "hours_use_time": 2,
      "usage_location": "FRA",
      "hours_electrical_consumption": 120
  }}'
```

Result : 

* The API will use an electrical consumption of 120 Watt/hours for 2 hours
* Usage impacts will be assessed for the French electrical mix impacts 


```json
{
  "gwp": {
    "other": {
      "value": 17.5,
      "significant_figures": 3,
      "min": 11.2,
      "max": 26.2
    },
    "use": {
      "value": 0.02,
      "significant_figures": 1,
      "min": 0.02,
      "max": 0.02
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
  '{{ endpoint }}/v1/component/cpu?verbose=false&allocation=TOTAL&criteria=gwp' \
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
    "other": {
      "value": 17.5,
      "significant_figures": 3,
      "min": 11.2,
      "max": 26.2
    },
    "use": {
      "value": 0.01,
      "significant_figures": 1,
      "min": 0.01,
      "max": 0.01
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  }
}
```

For further information see : [The explanation page on cpu](../Explanations/components/cpu.md)