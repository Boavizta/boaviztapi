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
  '{{ endpoint }}/v1/server/?archetype=compute_medium&verbose=false' 
  -H 'accept: application/json'
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
  "gwp": {
    "embedded": {
      "value": 661.28,
      "significant_figures": 5,
      "min": 256.4,
      "max": 1980.9,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 6937.1,
      "significant_figures": 5,
      "min": 193.81,
      "max": 48551
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "embedded": {
      "value": 0.13048,
      "significant_figures": 5,
      "min": 0.060814,
      "max": 0.24361,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.00117259,
      "significant_figures": 6,
      "min": 0.000111569,
      "max": 0.0113943
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "embedded": {
      "value": 9035.9,
      "significant_figures": 5,
      "min": 3480,
      "max": 25941,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 235000,
      "significant_figures": 5,
      "min": 109.55,
      "max": 20086000
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
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
        "value": 661.28,
        "significant_figures": 5,
        "min": 256.4,
        "max": 1980.9,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 6937.1,
        "significant_figures": 5,
        "min": 193.81,
        "max": 48551
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    }
  },
  "verbose": {
    "duration": {
      "value": 35040,
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
        "value": 35040,
        "unit": "hours"
      }
    },
    "CPU-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 65.757,
            "significant_figures": 5,
            "min": 14.835,
            "max": 297.63,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 4852.9,
            "significant_figures": 5,
            "min": 146.86,
            "max": 28903
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        }
      },
      "units": {
        "value": 2,
        "status": "ARCHETYPE",
        "min": 1,
        "max": 4
      },
      "core_units": {
        "value": 24,
        "status": "ARCHETYPE",
        "min": 16,
        "max": 32
      },
      "die_size_per_core": {
        "value": 0.48162162162162164,
        "status": "COMPLETED",
        "unit": "cm2",
        "source": "Average for all families",
        "min": 0.15,
        "max": 1.02
      },
      "duration": {
        "value": 35040,
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
        "value": 35040,
        "status": "COMPLETED",
        "unit": "hours",
        "source": "from device",
        "min": 35040,
        "max": 35040
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
        "value": 6,
        "status": "ARCHETYPE",
        "min": 4,
        "max": 8
      },
      "capacity": {
        "value": 16,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 8,
        "max": 32
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
        "value": 35040,
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
        "value": 35040,
        "status": "COMPLETED",
        "unit": "hours",
        "source": "from device",
        "min": 35040,
        "max": 35040
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
        "value": 500,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 100,
        "max": 2000
      },
      "density": {
        "value": 54.8842105263158,
        "status": "COMPLETED",
        "unit": "GB/cm2",
        "source": "Average of 19 rows",
        "min": 16.4,
        "max": 128
      },
      "duration": {
        "value": 35040,
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
            "max": 243,
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
        "value": 2,
        "status": "ARCHETYPE",
        "min": 1,
        "max": 2
      },
      "unit_weight": {
        "value": 2.99,
        "status": "ARCHETYPE",
        "unit": "kg",
        "min": 1,
        "max": 5
      },
      "duration": {
        "value": 35040,
        "unit": "hours"
      }
    },
    "CASE-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 150,
            "significant_figures": 5,
            "min": 85.9,
            "max": 150,
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
        "value": 35040,
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
        "value": 35040,
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
      "value": 1,
      "status": "ARCHETYPE",
      "unit": "/1",
      "min": 1,
      "max": 1
    },
    "hours_life_time": {
      "value": 35040,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 35040,
      "max": 35040
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
      "die_size_per_core": 0.245
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
  "gwp": {
    "embedded": {
      "value": 1501.4,
      "significant_figures": 5,
      "min": 1501.4,
      "max": 1501.4,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 10317,
      "significant_figures": 5,
      "min": 563.41,
      "max": 36960
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "embedded": {
      "value": 0.16588,
      "significant_figures": 5,
      "min": 0.16588,
      "max": 0.16588,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.00174387,
      "significant_figures": 6,
      "min": 0.000324327,
      "max": 0.00867403
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "embedded": {
      "value": 19475,
      "significant_figures": 5,
      "min": 19475,
      "max": 19475,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 349500,
      "significant_figures": 5,
      "min": 318.45,
      "max": 15290000
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
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
  "impacts": {
    "gwp": {
      "other": {
        "value": 660,
        "significant_figures": 2,
        "min": 350,
        "max": 1100
      },
      "use": {
        "value": 220,
        "significant_figures": 2,
        "min": 220,
        "max": 220
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "other": {
        "value": 0.13,
        "significant_figures": 2,
        "min": 0.064,
        "max": 0.22
      },
      "use": {
        "value": 0.000107,
        "significant_figures": 3,
        "min": 0.000107,
        "max": 0.000107
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    },
    "pe": {
      "other": {
        "value": 9000,
        "significant_figures": 2,
        "min": 4600,
        "max": 15000
      },
      "use": {
        "value": 24800,
        "significant_figures": 3,
        "min": 24800,
        "max": 24800
      },
      "unit": "MJ",
      "description": "Consumption of primary energy"
    }
  },
  "verbose": {
    ...
    "avg_power": {
      "value": 250,
      "status": "INPUT",
      "unit": "W"
    },
    "usage_location": {
      "value": "FRA",
      "status": "INPUT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    },
    "use_time": {
      "value": 8785,
      "status": "INPUT",
      "unit": "hours"
    },
    "gwp_factor": {
      "value": 0.098,
      "status": "COMPLETED",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
      "min": 0.098,
      "max": 0.098
    },
    "adp_factor": {
      "value": 4.86e-08,
      "status": "COMPLETED",
      "unit": "kg Sbeq/kWh",
      "source": "ADEME BASE IMPACT",
      "min": 4.86e-08,
      "max": 4.86e-08
    },
    "pe_factor": {
      "value": 11.289,
      "status": "COMPLETED",
      "unit": "MJ/kWh",
      "source": "ADPf / (1-%renewable_energy)",
      "min": 11.289,
      "max": 11.289
    }
  }
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
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 165.32,
        "significant_figures": 5,
        "min": 64.099,
        "max": 495.23,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 595.3,
        "significant_figures": 5,
        "min": 273.24,
        "max": 1407.3
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "embedded": {
        "value": 0.032619,
        "significant_figures": 5,
        "min": 0.015204,
        "max": 0.060903,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 0.0002951,
        "significant_figures": 6,
        "min": 0.000135448,
        "max": 0.000697639
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    },
    "pe": {
      "embedded": {
        "value": 2259,
        "significant_figures": 5,
        "min": 870.01,
        "max": 6485.2,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 68575,
        "significant_figures": 5,
        "min": 31476,
        "max": 162120
      },
      "unit": "MJ",
      "description": "Consumption of primary energy"
    }
  },
  "verbose": {
    "duration": {
      "value": 8760,
      "unit": "hours"
    },
    ...
    "units": {
      "value": 1,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 1
    }
  }
}
```

For further information see : [The explanation page on servers](../Explanations/devices/server.md)