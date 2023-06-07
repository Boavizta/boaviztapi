# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of cloud instance (AWS use case).

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws?instance_type=a1.xlarge' | jq`)_

## Get available cloud instances

This query returns the list of available aws instances 

Query: 
```bash
# Query the available aws instances
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance/all_instances?provider=aws' \
  -H 'accept: application/json'
```

Results:

```json
[
  "r6g.xlarge",
  "c5a.4xlarge",
  "r5b.xlarge",
  "r5dn.metal",
  "r5ad.12xlarge",
  "r6gd.xlarge",
  ...
  "m5ad.2xlarge",
  "r6g.medium"
]
```

## Get the impacts of a cloud instance with default usage data

This query returns :

* Only gwp impact is compute since ```criteria=gwp```
* The usage impact for 1 year (since ```duration=8760```) of compute at 50% of load for a ```r6g.medium``` instance type in europe
* The embedded impacts of a ```r6g.medium``` allocated on one year (since ```duration=8760```).

Query:

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance?provider=aws&instance_type=r6g.medium&verbose=false&duration=8760&criteria=gwp' \
  -H 'accept: application/json'
```

Results:
```json
{
  "gwp": {
    "embedded": {
      "value": 5.3431,
      "significant_figures": 5,
      "min": 194.02,
      "max": 590.64,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 17.747,
      "significant_figures": 5,
      "min": 62.027,
      "max": 4069
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  }
}
```

## Get the values used to assess the impacts of each component
This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components (including usage) and the value of the attributes used for the calculation.

* Both adp and gwp impacts are compute since ```criteria=adp&criteria=gwp```

Query :

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance?cloud_provider=aws&instance_type=r6g.medium&verbose=true&duration=8760&criteria=gwp&criteria=adp' \
  -H 'accept: application/json'
```

Response :

```json
{
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 5.3431,
        "significant_figures": 5,
        "min": 194.02,
        "max": 590.64,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 17.747,
        "significant_figures": 5,
        "min": 62.027,
        "max": 4069
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "embedded": {
        "value": 0.00057378,
        "significant_figures": 5,
        "min": 0.025378,
        "max": 0.053353,
        "warnings": [
          "End of life is not included in the calculation"
        ]
      },
      "use": {
        "value": 2.99981e-06,
        "significant_figures": 6,
        "min": 3.57061e-05,
        "max": 0.000954948
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    }
  },
  "verbose": {
    "duration": {
      "value": 8760,
      "unit": "hours"
    },
    "ASSEMBLY-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 1.67,
            "significant_figures": 5,
            "min": 1.67,
            "max": 1.67,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 3.525e-07,
            "significant_figures": 5,
            "min": 3.525e-07,
            "max": 3.525e-07,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "duration": {
        "value": 8760,
        "unit": "hours"
      }
    },
    "CPU-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 2.7514,
            "significant_figures": 5,
            "min": 2.7514,
            "max": 2.7514,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 369.96,
            "significant_figures": 5,
            "min": 22.393,
            "max": 1101.7
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0.0051001,
            "significant_figures": 5,
            "min": 0.0051001,
            "max": 0.0051001,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 6.2535e-05,
            "significant_figures": 5,
            "min": 1.289e-05,
            "max": 0.00025856
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
        "value": 64,
        "status": "COMPLETED",
        "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": 64,
        "max": 64
      },
      "die_size_per_core": {
        "value": 0.007125,
        "status": "COMPLETED",
        "unit": "cm2",
        "source": "die_size/core_units",
        "min": 0.007125,
        "max": 0.007125
      },
      "die_size": {
        "value": 0.456,
        "status": "COMPLETED",
        "unit": "cm2",
        "source": "https://en.wikichip.org/wiki/annapurna_labs/alpine/alc12b00 : Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": 0.456,
        "max": 0.456
      },
      "model_range": {
        "value": "Graviton2",
        "status": "COMPLETED",
        "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": "Graviton2",
        "max": "Graviton2"
      },
      "manufacturer": {
        "value": "Annapurna Labs",
        "status": "COMPLETED",
        "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": "Annapurna Labs",
        "max": "Annapurna Labs"
      },
      "family": {
        "value": "Graviton2",
        "status": "COMPLETED",
        "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": "Graviton2",
        "max": "Graviton2"
      },
      "name": {
        "value": "Graviton2",
        "status": "COMPLETED",
        "source": "fuzzy match",
        "min": "Graviton2",
        "max": "Graviton2"
      },
      "tdp": {
        "value": 150,
        "status": "COMPLETED",
        "unit": "W",
        "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
        "min": 150,
        "max": 150
      },
      "duration": {
        "value": 8760,
        "unit": "hours"
      },
      "avg_power": {
        "value": 111.14041865330084,
        "status": "COMPLETED",
        "unit": "W",
        "min": 111.14041865330084,
        "max": 111.14041865330084,
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
      "workloads": {
        "value": [
          {
            "load_percentage": 0,
            "power_watt": 18
          },
          {
            "load_percentage": 10,
            "power_watt": 48
          },
          {
            "load_percentage": 50,
            "power_watt": 112.5
          },
          {
            "load_percentage": 100,
            "power_watt": 153
          }
        ],
        "status": "COMPLETED",
        "unit": "workload_rate:W"
      },
      "params": {
        "value": {
          "a": 85.60000000000001,
          "b": 0.05249636311684195,
          "c": 25.813271558070987,
          "d": -7.095606671334251
        },
        "status": "COMPLETED",
        "source": "From TDP"
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
    },
    "RAM-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 247.18,
            "significant_figures": 5,
            "min": 139.45,
            "max": 471.44,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 484.03,
            "significant_figures": 5,
            "min": 29.297,
            "max": 1441.4
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0.01324,
            "significant_figures": 5,
            "min": 0.010155,
            "max": 0.019662,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 8.1817e-05,
            "significant_figures": 5,
            "min": 1.6865e-05,
            "max": 0.00033828
          },
          "unit": "kgSbeq",
          "description": "Use of minerals and fossil ressources"
        }
      },
      "units": {
        "value": 16,
        "status": "ARCHETYPE",
        "min": 16,
        "max": 16
      },
      "capacity": {
        "value": 32,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 32,
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
        "value": 8760,
        "unit": "hours"
      },
      "avg_power": {
        "value": 9.088,
        "status": "COMPLETED",
        "unit": "W",
        "min": 9.088,
        "max": 9.088,
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
          "a": 9.088
        },
        "status": "COMPLETED",
        "source": "(ram_electrical_factor_per_go : 0.284) * (ram_capacity: 32.0) "
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
    },
    "SSD-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 0,
            "significant_figures": 5,
            "min": 0,
            "max": 0,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0,
            "significant_figures": 5,
            "min": 0,
            "max": 0,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgSbeq",
          "description": "Use of minerals and fossil ressources"
        }
      },
      "units": {
        "value": 0,
        "status": "ARCHETYPE",
        "min": 0,
        "max": 0
      },
      "capacity": {
        "value": 0,
        "status": "ARCHETYPE",
        "unit": "GB",
        "min": 0,
        "max": 0
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
        "value": 8760,
        "unit": "hours"
      }
    },
    "POWER_SUPPLY-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 36.329,
            "significant_figures": 5,
            "min": 12.15,
            "max": 60.75,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0.012409,
            "significant_figures": 5,
            "min": 0.00415,
            "max": 0.02075,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgSbeq",
          "description": "Use of minerals and fossil ressources"
        }
      },
      "units": {
        "value": 2,
        "status": "ARCHETYPE",
        "min": 2,
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
        "value": 8760,
        "unit": "hours"
      }
    },
    "CASE-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 37.5,
            "significant_figures": 5,
            "min": 21.475,
            "max": 37.5,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0.00505,
            "significant_figures": 5,
            "min": 0.00505,
            "max": 0.006918,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "case_type": {
        "value": "rack",
        "status": "ARCHETYPE"
      },
      "duration": {
        "value": 8760,
        "unit": "hours"
      }
    },
    "MOTHERBOARD-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 16.525,
            "significant_figures": 5,
            "min": 16.525,
            "max": 16.525,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "embedded": {
            "value": 0.0009225,
            "significant_figures": 5,
            "min": 0.0009225,
            "max": 0.0009225,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": "not implemented",
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
      "duration": {
        "value": 8760,
        "unit": "hours"
      }
    },
    "avg_power": {
      "value": 341.20884,
      "status": "COMPLETED",
      "unit": "W",
      "min": 307.8576,
      "max": 410.4768
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
    "instance_per_server": {
      "value": 64,
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

## Get the impacts of a cloud instance with custom usage data

In this query we override default usage data with your custom data for ```r6g.medium``` instance type

*Note: you can override zero to many attributes.*

Query:

```bash
# Query the data for `r6g.medium` with custom usage value
curl -X 'POST' \
  '{{ endpoint }}/v1/cloud/instance?verbose=false&duration=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": "aws",
    "instance_type": "r6g.medium",
    "usage": {
       "usage_location": "FRA",
       "time_workload": [
          {
            "time_percentage": 50,
            "load_percentage": 0
          },
          {
            "time_percentage": 50,
            "load_percentage": 50
          }
       ]}
    }'
```


* Since no criteria flags are specified, the API returns the impacts of the instance for the default criteria (adp, pe, gwp). 
* Since duration is set at 2 and time_workload is provided, the query usage can be translated as such :

```I used a r6g.medium in a french data center for 2 hours half of the time in IDLE mode and half of the time at 50% of workload```

Results:

```json
{
  "gwp": {
    "embedded": {
      "value": 0.0012199,
      "significant_figures": 5,
      "min": 0.044297,
      "max": 0.13485,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.00085713,
      "significant_figures": 5,
      "min": 0.049495,
      "max": 0.065993
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "embedded": {
      "value": 1.31e-07,
      "significant_figures": 5,
      "min": 5.7941e-06,
      "max": 1.2181e-05,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 4.24891e-10,
      "significant_figures": 6,
      "min": 2.45351e-08,
      "max": 3.27134e-08
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "embedded": {
      "value": 0.015881,
      "significant_figures": 5,
      "min": 0.57578,
      "max": 1.7325,
      "warnings": [
        "End of life is not included in the calculation"
      ]
    },
    "use": {
      "value": 0.098736,
      "significant_figures": 5,
      "min": 5.7015,
      "max": 7.602
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
```

For further information see : [The explanation page on cloud](../Explanations/devices/cloud.md)
