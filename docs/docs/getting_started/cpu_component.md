# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of a CPU. See the detailed documentation for the other components.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'https://api.boavizta.org/v1/cloud/aws/all_instances' | jq`)_

## Get the impacts from cpu name

In this query, we use the cpu name to evaluate its impact.

Query : 

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=false&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

This query returns :

- The total manufacture impact (gwp, pe, adp) of the CPU
- The usage impact (gwp, pe, adp) of the CPU for one year (default)

Result :

```json
{
  "gwp": {
    "manufacture": 23.8,
    "use": 310,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 353,
    "use": 10670,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.02,
    "use": 5.32e-05,
    "unit": "kgSbeq"
  }
}

```

## Get the values used to measure the impacts of the cpu

This is the same query as before. However, you add the `verbose=true` flag to get the value of the attributes used for the calculation.

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=true&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
}'
```

This query returns :

* The total manufacture impact (gwp, pe, adp) of the CPU
* The CPU characteristics used to evaluate these impacts
* The usage impact (gwp, pe, adp) of the CPU for one year (default)

Result :

You can see that the API have completed the needed value from the cpu name. We parse and fuzzymatch the cpu ```name``` with our dataset of cpu to identify ```model_range```, ```manufacturer``` and ```family```.
The ```die_size_per_core``` is completed from the cpu family.

The usage impact have been evaluated using a default level of workload of 50% with the consumption profile of a xeon gold (completed from cpu ```name```.

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 23.8,
      "use": 310,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 353,
      "use": 10670,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.02,
      "use": 5.32e-05,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "units": 1,
    "manufacture_impacts": {
      "gwp": {
        "value": 23.8,
        "unit": "kgCO2eq"
      },
      "pe": {
        "value": 353,
        "unit": "MJ"
      },
      "adp": {
        "value": 0.02,
        "unit": "kgSbeq"
      }
    },
    "core_units": {
      "value": 28,
      "unit": "none",
      "status": "COMPLETED",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)"
    },
    "die_size_per_core": {
      "value": 0.248,
      "unit": "cm2",
      "status": "COMPLETED",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)"
    },
    "model_range": {
      "value": "xeon gold",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    },
    "manufacturer": {
      "value": "intel",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    },
    "family": {
      "value": "skylake",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    },
    "USAGE": {
      "usage_impacts": {
        "gwp": {
          "value": 310,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 10670,
          "unit": "MJ"
        },
        "adp": {
          "value": 5.32e-05,
          "unit": "kgSbeq"
        }
      },
      "hours_electrical_consumption": {
        "value": 94.62364134445255,
        "unit": "W",
        "status": "COMPLETED",
        "source": null
      },
      "time_workload": {
        "value": 50,
        "unit": "%",
        "status": "DEFAULT",
        "source": null
      },
      "usage_location": {
        "value": "EEE",
        "unit": "CodSP3 - NCS Country Codes - NATO",
        "status": "DEFAULT",
        "source": null
      },
      "adp_factor": {
        "value": 6.42e-08,
        "unit": "KgSbeq/kWh",
        "status": "COMPLETED",
        "source": {
          "1": "ADEME BASE IMPACT"
        }
      },
      "gwp_factor": {
        "value": 0.38,
        "unit": "kgCO2e/kWh",
        "status": "COMPLETED",
        "source": {
          "1": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries"
        }
      },
      "pe_factor": {
        "value": 12.874,
        "unit": "MJ/kWh",
        "status": "COMPLETED",
        "source": {
          "1": "ADPf / (1-%renewable_energy)"
        }
      },
      "use_time": {
        "value": 8760,
        "unit": "hours",
        "status": "DEFAULT",
        "source": null
      },
      "params": {
        "value": {
          "a": 35.5688,
          "b": 0.2438,
          "c": 9.6694,
          "d": -0.6087
        },
        "unit": "none",
        "status": "COMPLETED",
        "source": "From CPU model range"
      }
    }
  }
}
```

## Get the impacts from custom cpu characteristics

In this query, we give some characteristics to describe the CPU. 

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=true&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
 -d '{
      "core_units": 24,
      "family": "Skylake"
      }'
```

This query returns :

* The total manufacture impact (gwp, pe, adp) of the CPU
* The usage impact (gwp, pe, adp) of the CPU for one year (default)

Result :

Since only lowercase are used, the API will correct Skylake to skylake (CHANGED). And complete the missing attribute from the given attributes (COMPLETED) or by default ones (DEFAULT).

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 23.8,
      "use": 610,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 353,
      "use": 20550,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.02,
      "use": 0.000102,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "units": 1,
    "manufacture_impacts": {
      "gwp": {
        "value": 23.8,
        "unit": "kgCO2eq"
      },
      "pe": {
        "value": 353,
        "unit": "MJ"
      },
      "adp": {
        "value": 0.02,
        "unit": "kgSbeq"
      }
    },
    "core_units": {
      "value": 24,
      "unit": "none",
      "status": "INPUT",
      "source": null
    },
    "die_size_per_core": {
      "value": 0.289,
      "unit": "cm2",
      "status": "COMPLETED",
      "source": {
        "1": "https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)"
      }
    },
    "family": {
      "value": "skylake",
      "unit": "none",
      "status": "CHANGED",
      "source": null
    },
   ...
}

```

## Get the impacts from custom cpu usage using an electrical consumption

In this query we set a custom usage to an ```intel xeon gold 6134```. The average electrical consumption is given.

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=false&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134"
  "usage":{
      "hours_use_time": 2,
      "usage_location": "FRA",
      "hours_electrical_consumption": 120
  }}'
```

Result : 

* The API will use an electrical consumption of 120 Watt/hours for 2 hours
* Usage impacts will be measure for the French electrical mix impacts 


```json
{
  "gwp": {
    "manufacture": 23.8,
    "use": 0.02,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 353,
    "use": 2,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.02,
    "use": 8e-09,
    "unit": "kgSbeq"
  }
}

```


## Get the impacts from custom cpu usage using a workload

In this query we set a custom usage to an ```intel xeon gold 6134``` with a TDP of 130 Watt. The average electrical consumption is retrieved.

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=false&allocation=TOTAL' \
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
    "manufacture": 23.8,
    "use": 0.02,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 353,
    "use": 2,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.02,
    "use": 8e-09,
    "unit": "kgSbeq"
  }
}
```

For further information see : [The explanation page on cpu](../Explanations/components/cpu.md)