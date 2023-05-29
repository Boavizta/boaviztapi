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

- The total embedded impacts (for gwp, pe, adp) of the server
- The usage impacts (for gwp, pe, adp) of the server for one year (default)
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

Results:

```json
{
  "gwp": {
    "other": {
      "value": 660,
      "significant_figures": 2,
      "min": 350,
      "max": 1100
    },
    "use": {
      "value": 1700,
      "significant_figures": 2,
      "min": 48,
      "max": 9700
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
      "value": 0.000293,
      "significant_figures": 3,
      "min": 2.78e-05,
      "max": 0.00285
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
      "value": 58760,
      "significant_figures": 4,
      "min": 27.39,
      "max": 5021000
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
}

```

## Get the values used to assess the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components and the value of the attributes used for the calculation. 
This query returns will only compute the gwp impacts since we add the `criteria=gwp` flags.


Query:

```bash
# Query the data for `compute_medium`
curl -X 'GET' \
  '{{ endpoint }}/v1/server/?archetype=compute_medium&verbose=true&criteria=gwp' \
  -H 'accept: application/json'
```

It returns :

- The **total** impacts of manufacturing (gwp) for each component (like RAM, CPU, SSD a.s.o)
- The impacts (gwp) of usage at server level for one year
- The impacts (gwp) of usage for CPU and RAM for one year
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```JSON
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
        "value": 1700,
        "significant_figures": 2,
        "min": 48,
        "max": 9700
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    }
  },
  "verbose": {
    "ASSEMBLY-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 6.68,
            "significant_figures": 3,
            "min": 6.68,
            "max": 6.68
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
      }
    },
    "CPU-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 64.7,
            "significant_figures": 3,
            "min": 12.3,
            "max": 298
          },
          "use": {
            "value": 1200,
            "significant_figures": 2,
            "min": 37,
            "max": 5700
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
        "value": 0.47078947368421054,
        "status": "COMPLETED",
        "unit": "mm2",
        "source": "Average for all families",
        "min": 0.07,
        "max": 1.02
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
      }
    },
    "RAM-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 200,
            "significant_figures": 2,
            "min": 130,
            "max": 280
          },
          "use": {
            "value": 91,
            "significant_figures": 2,
            "min": 3.7,
            "max": 290
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
      "use_time": {
        "value": 8760,
        "status": "ARCHETYPE",
        "unit": "hours",
        "min": 8760,
        "max": 8760
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
        "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries",
        "min": 0.023,
        "max": 0.9
      }
    },
    "SSD-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 26,
            "significant_figures": 2,
            "min": 20,
            "max": 41
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
      }
    },
    "POWER_SUPPLY-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 145,
            "significant_figures": 3,
            "min": 24.3,
            "max": 243
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
      }
    },
    "CASE-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 150,
            "significant_figures": 3,
            "min": 85.9,
            "max": 150
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
      }
    },
    "MOTHERBOARD-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 66.1,
            "significant_figures": 3,
            "min": 66.1,
            "max": 66.1
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
    "use_time": {
      "value": 8760,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 8760,
      "max": 8760
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
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries",
      "min": 0.023,
      "max": 0.9
    }
  }
}
```

## Retrieve the impacts of a _custom_ server

In this query, you provide a specific configuration of the machine. Missing attributes or component will be replaced by the archetype specify with the flag ```archetype=compute_medium```.

The API returns impacts, to reflect your _own_ server configuration. Since no criteria flags are specified, the API returns the impacts of the server for the default criteria (adp, pe, gwp).

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
    "other": {
      "value": 1500,
      "significant_figures": 2,
      "min": 1500,
      "max": 1500
    },
    "use": {
      "value": 2600,
      "significant_figures": 2,
      "min": 140,
      "max": 7300
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "other": {
      "value": 0.17,
      "significant_figures": 2,
      "min": 0.17,
      "max": 0.17
    },
    "use": {
      "value": 0.000436,
      "significant_figures": 3,
      "min": 8.08e-05,
      "max": 0.00217
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "other": {
      "value": 19000,
      "significant_figures": 2,
      "min": 19000,
      "max": 19000
    },
    "use": {
      "value": 87380,
      "significant_figures": 4,
      "min": 79.61,
      "max": 3823000
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
}

```

## Retrieve the impacts with a custom power consumption

In this query, we use the default server configuration of a ```compute_medium``` but provide a specific usage of the machine.

In this specific case, the average power consumption of the machine is given by the user (```avg_powers``)

The API returns impacts, updated to reflect your own server usage. Since no criteria flags are specified, the API returns the impacts of the server for the default criteria (adp, pe, gwp).

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=true&archetype=compute_medium' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {},
  "configuration": {},
  "usage":{
     "years_use_time": 1,
     "days_use_time": 1,
     "hours_use_time": 1,
     "usage_location": "FRA",
     "avg_power": 250
    }
  }'
```

* The server is assessed with the specific impacts of the French electrical grid.
* The server is assessed for a usage of 1 year, 1 day, 1 hour. It corresponds to 8785 hours.
* The average electrical consumption per hour is 250 W/hour.

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

In this case the average is unknown electrical consumption is unknown. In this case, we use the level of workload (```time_workload```) of the machine as a proxy for the power consumption.

Query : 
```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {},
  "configuration": {},
  "usage":{
     "years_use_time": 1,
     "days_use_time": 1,
     "hours_use_time": 1,
     "usage_location": "FRA",
     "time_workload": 90
    }
  }'
```

* The API will create a consumption profile based on the default characteristics and apply it for an average level of workload of 90%

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
        "value": 600,
        "significant_figures": 2,
        "min": 270,
        "max": 1400
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
        "value": 0.000296,
        "significant_figures": 3,
        "min": 0.000136,
        "max": 0.0007
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
        "value": 68770,
        "significant_figures": 4,
        "min": 31570,
        "max": 162600
      },
      "unit": "MJ",
      "description": "Consumption of primary energy"
    }
  },
  "verbose": {
    ...
    "avg_power": {
      "value": 693.44072,
      "status": "COMPLETED",
      "unit": "W",
      "min": 318.28319999999997,
      "max": 1639.3472000000002
    },
    "time_workload": {
      "value": 90,
      "status": "INPUT",
      "unit": "%"
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
    "other_consumption_ratio": {
      "value": 0.33,
      "status": "ARCHETYPE",
      "unit": "ratio /1",
      "min": 0.2,
      "max": 0.6
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

For further information see : [The explanation page on servers](../Explanations/devices/server.md)