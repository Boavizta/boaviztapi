# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/server/?archetype=compute_medium' | jq`)_

## Get the impacts of a compute medium server

This is the simplest possible query. It returns the impacts of a _standard_ (i.e. predefined) server configuration (compute_medium).

Query: 
```bash
# Query the data for `compute_medium`
curl -X 'GET' \
  '{{ endpoint }}/v1/server/?archetype=compute_medium&verbose=false' -H 'accept: application/json'
```
This query returns :

- The impacts for the default criteria (gwp, pe, adp) since no impact is specified
- The total embedded impacts of the server, since no duration is given
- The usage impacts of the server during its life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

Results:

```json
{
    "detail": "compute_medium not found"
}
```

## Get the values used to assess the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components and the value of the attributes used for the calculation. 
This query will only compute the gwp impacts since we add the `criteria=gwp` flags.

Query:

```bash
# Query the data for `compute_medium`
curl -X 'GET' \
  '{{ endpoint }}/v1/server/?archetype=compute_medium&verbose=true&criteria=gwp' \
  -H 'accept: application/json'
```

It will return:

- The **total** embedded impacts for each component (like RAM, CPU, SSD a.s.o)
- Since no duration is given, the usage impacts of the server during the life duration of the server
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```JSON
{
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 625.51,
        "significant_figures": 5,
        "min": 252.18,
        "max": 2010.6,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 6937.1,
        "significant_figures": 5,
        "min": 193.81,
        "max": 48551.0
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    }
  },
  "verbose": {
    "duration": {
      "value": 35040.0,
      "unit": "hours"
    },
    "ASSEMBLY-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 6.68,
            "significant_figures": 5,
            "min": 6.68,
            "max": 6.68,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      }
    },
    "CPU-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 29.986,
            "significant_figures": 5,
            "min": 10.619,
            "max": 327.26,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 4852.9,
            "significant_figures": 5,
            "min": 146.86,
            "max": 28903.0
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        }
      },
      "units": {
        "value": 2.0,
        "status": "ARCHETYPE",
        "min": 1.0,
        "max": 4.0
      },
      "die_size": {
        "value": 248,
        "status": "COMPLETED",
        "unit": "mm2",
        "source": "Average value for all families",
        "min": 26,
        "max": 364
      },
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      },
      "avg_power": {
        "value": 182.23023303189055,
        "status": "COMPLETED",
        "unit": "W",
        "min": 182.23023303189055,
        "max": 182.23023303189055,
        "warnings": [
          "value for one cpu unit"
        ]
      },
      "time_workload": {
        "value": 50.0,
        "status": "ARCHETYPE",
        "unit": "%",
        "min": 0.0,
        "max": 100.0
      },
      "usage_location": {
        "value": "EEE",
        "status": "DEFAULT",
        "unit": "CodSP3 - NCS Country Codes - NATO"
      },
      "use_time_ratio": {
        "value": 1.0,
        "status": "ARCHETYPE",
        "unit": "/1",
        "min": 1.0,
        "max": 1.0
      },
      "hours_life_time": {
        "value": 35040.0,
        "status": "COMPLETED",
        "unit": "hours",
        "source": "from device",
        "min": 35040.0,
        "max": 35040.0
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
      }
    },
    "RAM-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 201.05,
            "significant_figures": 5,
            "min": 50.522,
            "max": 942.88,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 363.03,
            "significant_figures": 5,
            "min": 14.648,
            "max": 1441.4
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        }
      },
      "units": {
        "value": 6.0,
        "status": "ARCHETYPE",
        "min": 4.0,
        "max": 8.0
      },
      "capacity": {
        "value": 16.0,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 8.0,
        "max": 32.0
      },
      "density": {
        "value": 1.2443636363636363,
        "status": "COMPLETED",
        "unit": "GB/cm2",
        "source": "Average of 11 rows",
        "min": 0.625,
        "max": 2.375
      },
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      },
      "avg_power": {
        "value": 4.544,
        "status": "COMPLETED",
        "unit": "W",
        "min": 4.544,
        "max": 4.544,
        "warnings": [
          "value for one ram strip"
        ]
      },
      "time_workload": {
        "value": 50.0,
        "status": "ARCHETYPE",
        "unit": "%",
        "min": 0.0,
        "max": 100.0
      },
      "usage_location": {
        "value": "EEE",
        "status": "DEFAULT",
        "unit": "CodSP3 - NCS Country Codes - NATO"
      },
      "use_time_ratio": {
        "value": 1.0,
        "status": "ARCHETYPE",
        "unit": "/1",
        "min": 1.0,
        "max": 1.0
      },
      "hours_life_time": {
        "value": 35040.0,
        "status": "COMPLETED",
        "unit": "hours",
        "source": "from device",
        "min": 35040.0,
        "max": 35040.0
      },
      "params": {
        "value": {
          "a": 4.544
        },
        "status": "COMPLETED",
        "source": "(ram_electrical_factor_per_go : 0.284) * (ram_capacity: 16.0) "
      },
      "gwp_factor": {
        "value": 0.38,
        "status": "DEFAULT",
        "unit": "kg CO2eq/kWh",
        "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
        "min": 0.023,
        "max": 1.13161
      }
    },
    "SSD-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 26.382,
            "significant_figures": 5,
            "min": 8.0588,
            "max": 274.63,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "capacity": {
        "value": 500.0,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 100.0,
        "max": 2000.0
      },
      "density": {
        "value": 54.8842105263158,
        "status": "COMPLETED",
        "unit": "GB/cm2",
        "source": "Average of 19 rows",
        "min": 16.4,
        "max": 128.0
      },
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      }
    },
    "POWER_SUPPLY-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 145.31,
            "significant_figures": 5,
            "min": 24.3,
            "max": 243.0,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        }
      },
      "units": {
        "value": 2.0,
        "status": "ARCHETYPE",
        "min": 1.0,
        "max": 2.0
      },
      "unit_weight": {
        "value": 2.99,
        "status": "ARCHETYPE",
        "unit": "kg",
        "min": 1.0,
        "max": 5.0
      },
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      }
    },
    "CASE-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 150.0,
            "significant_figures": 5,
            "min": 85.9,
            "max": 150.0,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "case_type": {
        "value": "rack",
        "status": "ARCHETYPE"
      },
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      }
    },
    "MOTHERBOARD-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 66.1,
            "significant_figures": 5,
            "min": 66.1,
            "max": 66.1,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "duration": {
        "value": 35040.0,
        "unit": "hours"
      }
    },
    "avg_power": {
      "value": 520.99292,
      "status": "COMPLETED",
      "unit": "W",
      "min": 240.48719999999997,
      "max": 1224.4352
    },
    "usage_location": {
      "value": "EEE",
      "status": "DEFAULT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    },
    "use_time_ratio": {
      "value": 1.0,
      "status": "ARCHETYPE",
      "unit": "/1",
      "min": 1.0,
      "max": 1.0
    },
    "hours_life_time": {
      "value": 35040.0,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 35040.0,
      "max": 35040.0
    },
    "other_consumption_ratio": {
      "value": 0.33,
      "status": "ARCHETYPE",
      "unit": "ratio /1",
      "min": 0.2,
      "max": 0.6
    },
    "gwp_factor": {
      "value": 0.38,
      "status": "DEFAULT",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
      "min": 0.023,
      "max": 1.13161
    },
    "units": {
      "value": 1,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 1
    }
  }
}
```

## Retrieve the impacts of a _custom_ server

In this query, you provide a specific configuration of the machine. Missing attributes or component will be replaced by the archetype specify with the flag ```archetype=compute_medium```.

The API returns impacts, to reflect your _own_ server configuration. 

Query : 
```bash

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=false&archetype=compute_medium' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {
    "type": "rack"
  },
  "configuration": {
    "cpu": {
      "units": 2,
      "core_units": 12,
      "die_size_per_core": 245
    },
    "ram": [
      {
        "units": 12,
        "capacity": 64,
        "density": 1.79
      }
    ],
    "disk": [
      {
        "units": 4,
        "type": "ssd",
        "capacity": 400,
        "density": 50.6
      }
    ],
    "power_supply": {
      "units": 2,
      "unit_weight": 2.99
    }
  }
}'
```

Result :
```json
{
    "detail": "compute_medium not found"
}
```

* Since no criteria flags are specified, the API returns the impacts of the server for the default criteria (adp, pe, gwp). 
* Since no duration is given, the API returns the impacts for the all life duration of the server.


## Retrieve the impacts with a custom power consumption

In this query, we use the default server configuration of a ```compute_medium``` but provide a specific usage of the machine.

In this specific case, the average power consumption of the machine is given by the user (```avg_powers``)

The API returns impacts, updated to reflect your own server usage. Since ```criteria=gwp&criteria=adp``` flags are specified, the API returns the impacts of the server for adp and gwp.

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=true&archetype=compute_medium&duration=8760' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {},
  "configuration": {},
  "usage":{
     "usage_location": "FRA",
     "avg_power": 250
    }
  }'
```

* Usage impacts are assessed with the specific impacts of the French electrical grid.
* The server impacts are assessed for a usage of 1 year (since duration is set at 8785 hours).
* The average electrical consumption per hour is 250 Watts/hour.
* Embedded impacts will be allocated on 1 year (since duration is set at 8785 hours).

Result :

```json
{
    "detail": "compute_medium not found"
}
```

## Retrieve the impacts with a custom workload

In this query, we use the default server configuration of a ```compute_medium``` but provide a specific usage of the machine.

In this case, the average electrical consumption is unknown. We use the level of workload (```time_workload```) of the machine as a proxy for the power consumption.

Query : 
```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=true&duration=8760' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {},
  "configuration": {},
  "usage":{
     "usage_location": "FRA",
     "time_workload": 90
    }
  }'
```

* The API will create a consumption profile based on the default characteristics and apply it for an average level of workload of 90%
* The server impacts are assessed for a usage of 1 year (since duration is set at 8785 hours).
* Embedded impacts will be allocated on 1 year (since duration is set at 8785 hours).

Result :
```json
{
    "detail": "compute_medium not found"
}
```

For further information see : [The explanation page on servers](../Explanations/devices/server.md)