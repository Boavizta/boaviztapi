# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/server/?archetype=platform_compute_medium' | jq`)_

## Get the impacts of a compute medium server

This is the simplest possible query. It returns the impacts of a _standard_ (i.e. predefined) server configuration (```platform_compute_medium```).

_note: if no archetype is specified, a default one will be used_

Query: 
```bash
# Query the data for `platform_compute_medium`
curl -X 'GET' \
  '{{ endpoint }}/v1/server/?archetype=platform_compute_medium&verbose=false' -H 'accept: application/json'
```

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 900.0,
                "min": 461.8,
                "max": 2089.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 8000.0,
                "min": 405.2,
                "max": 28890.0
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.14,
                "min": 0.09758,
                "max": 0.2132,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.0013,
                "min": 0.0002333,
                "max": 0.00678
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 13000.0,
                "min": 6138.0,
                "max": 27090.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 300000.0,
                "min": 229.0,
                "max": 11950000.0,
                "warnings": [
                    "Uncertainty from technical characteristics is very important. Results should be interpreted with caution (see min and max values)"
                ]
            }
        }
    }
}
```
</details>

This query returns :

- The impacts for the default criteria (gwp, pe, adp) since no impact criteria are specified
- The total embedded impacts of the server, since no duration is given
- The usage impacts of the server during its life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts

## Get the values used to assess the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components and the value of the attributes used for the calculation. 
This query will only compute the gwp impacts since we add the `criteria=gwp` flags.

Query:

```bash
# Query the data for `platform_compute_medium`
curl -X 'GET' \
  '{{ endpoint }}/v1/server/?archetype=platform_compute_medium&verbose=true&criteria=gwp' \
  -H 'accept: application/json'
```
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 900.0,
                "min": 461.8,
                "max": 2089.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 8000.0,
                "min": 405.2,
                "max": 28890.0
            }
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 6.68,
                        "min": 6.68,
                        "max": 6.68,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 40.0,
                        "min": 21.84,
                        "max": 163.6,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 10000.0,
                        "min": 587.5,
                        "max": 28900.0
                    }
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
                "max": 2.0
            },
            "die_size": {
                "value": 521.0,
                "status": "COMPLETED",
                "unit": "mm2",
                "source": "Average value for all families",
                "min": 41.2,
                "max": 3640.0
            },
            "duration": {
                "value": 35040.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 364.46,
                "status": "COMPLETED",
                "unit": "W",
                "min": 364.46,
                "max": 364.46
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 490.0,
                        "min": 209.2,
                        "max": 1179.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 8000.0,
                        "min": 263.7,
                        "max": 36040.0
                    }
                }
            },
            "units": {
                "value": 8.0,
                "status": "ARCHETYPE",
                "min": 6.0,
                "max": 10.0
            },
            "capacity": {
                "value": 32.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 32.0,
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
                "value": 72.704,
                "status": "COMPLETED",
                "unit": "W",
                "min": 54.52799999999999,
                "max": 90.88
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
            }
        },
        "SSD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 50.0,
                        "min": 23.53,
                        "max": 281.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "min": 1.0,
                "max": 2.0
            },
            "capacity": {
                "value": 1000.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 1000.0,
                "max": 1000.0
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 150.0,
                        "min": 48.6,
                        "max": 243.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 150.0,
                        "min": 85.9,
                        "max": 150.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
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
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 66.1,
                        "min": 66.1,
                        "max": 66.1,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
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
            "value": 581.42812,
            "status": "COMPLETED",
            "unit": "W",
            "min": 502.78559999999993,
            "max": 728.544
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

</details>

It will return:

- The **total** embedded impacts for each component (like RAM, CPU, SSD a.s.o) since no duration is given
- Since no duration is given, the usage impacts of the server during the life duration of the server
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)


## Retrieve the impacts of a _custom_ server

In this query, you provide a specific configuration of the machine. Missing attributes or component will be replaced by the archetype specify with the flag ```archetype=platform_compute_medium```.

The API returns impacts, to reflect your _own_ server configuration. 

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=false&archetype=platform_compute_medium' \
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

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 1606.0,
                "min": 1606.0,
                "max": 1606.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 10000.0,
                "min": 563.4,
                "max": 36960.0
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.1659,
                "min": 0.1659,
                "max": 0.1659,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.0017,
                "min": 0.0003243,
                "max": 0.008674
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 20880.0,
                "min": 20880.0,
                "max": 20880.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 300000.0,
                "min": 318.4,
                "max": 15290000.0,
                "warnings": [
                    "Uncertainty from technical characteristics is very important. Results should be interpreted with caution (see min and max values)"
                ]
            }
        }
    }
}
```

</details>

* Since no criteria flags are specified, the API returns the impacts of the server for the default criteria (adp, pe, gwp). 
* Since no duration is given, the API returns the impacts for the all life duration of the server.


## Retrieve the impacts with a custom power consumption

In this query, we use the default server configuration of a ```platform_compute_medium``` but provide a specific usage of the machine.

In this specific case, the average power consumption of the machine is given by the user (```avg_power```)

The API returns impacts, updated to reflect your own server usage. Since ```criteria=gwp&criteria=adp``` flags are specified, the API returns the impacts of the server for adp and gwp.

Query : 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/server/?verbose=true&archetype=platform_compute_medium&duration=8760' \
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

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 240.0,
                "min": 115.5,
                "max": 522.2,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 214.6,
                "min": 214.6,
                "max": 214.6
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.036,
                "min": 0.0244,
                "max": 0.05329,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.0001064,
                "min": 0.0001064,
                "max": 0.0001064
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 3200.0,
                "min": 1535.0,
                "max": 6773.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 24720.0,
                "min": 24720.0,
                "max": 24720.0
            }
        }
    },
    "verbose": {
        "duration": {
            "value": 8760.0,
            "unit": "hours"
        },
        "ASSEMBLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 1.67,
                        "min": 1.67,
                        "max": 1.67,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 3.525e-07,
                        "min": 3.525e-07,
                        "max": 3.525e-07,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 17.15,
                        "min": 17.15,
                        "max": 17.15,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CPU-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 10.0,
                        "min": 5.459,
                        "max": 40.91,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 2400.0,
                        "min": 146.9,
                        "max": 7226.0
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0102,
                        "min": 0.0102,
                        "max": 0.01021,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 0.0004,
                        "min": 8.454e-05,
                        "max": 0.001696
                    }
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 150.0,
                        "min": 89.96,
                        "max": 566.8,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 100000.0,
                        "min": 83.01,
                        "max": 2989000.0
                    }
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
                "max": 2.0
            },
            "die_size": {
                "value": 521.0,
                "status": "COMPLETED",
                "unit": "mm2",
                "source": "Average value for all families",
                "min": 41.2,
                "max": 3640.0
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 364.46,
                "status": "COMPLETED",
                "unit": "W",
                "min": 364.46,
                "max": 364.46
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
            },
            "adp_factor": {
                "value": 6.42317e-08,
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 1.324e-08,
                "max": 2.65575e-07
            },
            "pe_factor": {
                "value": 12.873,
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "source": "ADPf / (1-%renewable_energy)",
                "min": 0.013,
                "max": 468.15
            }
        },
        "RAM-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 120.0,
                        "min": 52.29,
                        "max": 294.7,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 1900.0,
                        "min": 65.92,
                        "max": 9009.0
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0066,
                        "min": 0.003808,
                        "max": 0.01229,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 0.0003,
                        "min": 3.795e-05,
                        "max": 0.002114
                    }
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 1600.0,
                        "min": 662.7,
                        "max": 3679.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 100000.0,
                        "min": 37.26,
                        "max": 3727000.0
                    }
                }
            },
            "units": {
                "value": 8.0,
                "status": "ARCHETYPE",
                "min": 6.0,
                "max": 10.0
            },
            "capacity": {
                "value": 32.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 32.0,
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
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 72.704,
                "status": "COMPLETED",
                "unit": "W",
                "min": 54.52799999999999,
                "max": 90.88
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
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 1.324e-08,
                "max": 2.65575e-07
            },
            "pe_factor": {
                "value": 12.873,
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "source": "ADPf / (1-%renewable_energy)",
                "min": 0.013,
                "max": 468.15
            }
        },
        "SSD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 12.0,
                        "min": 5.882,
                        "max": 70.24,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0004,
                        "min": 0.0002638,
                        "max": 0.002202,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 140.0,
                        "min": 72.55,
                        "max": 870.8,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "min": 1.0,
                "max": 2.0
            },
            "capacity": {
                "value": 1000.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 1000.0,
                "max": 1000.0
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "POWER_SUPPLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 36.0,
                        "min": 12.15,
                        "max": 60.75,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.012,
                        "min": 0.00415,
                        "max": 0.02075,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 530.0,
                        "min": 176.0,
                        "max": 880.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CASE-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 38.0,
                        "min": 21.48,
                        "max": 37.5,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.005,
                        "min": 0.00505,
                        "max": 0.006918,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 550.0,
                        "min": 307.2,
                        "max": 550.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "MOTHERBOARD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 16.52,
                        "min": 16.52,
                        "max": 16.52,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0009225,
                        "min": 0.0009225,
                        "max": 0.0009225,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 209.0,
                        "min": 209.0,
                        "max": 209.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "avg_power": {
            "value": 250.0,
            "status": "INPUT",
            "unit": "W"
        },
        "usage_location": {
            "value": "FRA",
            "status": "INPUT",
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
        "gwp_factor": {
            "value": 0.098,
            "status": "COMPLETED",
            "unit": "kg CO2eq/kWh",
            "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
            "min": 0.098,
            "max": 0.098
        },
        "adp_factor": {
            "value": 4.85798e-08,
            "status": "COMPLETED",
            "unit": "kg Sbeq/kWh",
            "source": "ADEME Base IMPACTS \u00ae",
            "min": 4.85798e-08,
            "max": 4.85798e-08
        },
        "pe_factor": {
            "value": 11.289,
            "status": "COMPLETED",
            "unit": "MJ/kWh",
            "source": "ADPf / (1-%renewable_energy)",
            "min": 11.289,
            "max": 11.289
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

</details>

* Usage impacts are assessed with the specific impacts of the French electrical grid.
* The server impacts are assessed for a usage of 1 year (since duration is set at 8785 hours).
* The average electrical consumption per hour is 250 Watts/hour.
* Embedded impacts will be allocated on 1 year (since duration is set at 8785 hours).


## Retrieve the impacts with a custom workload

In this query, we use the default server configuration of a ```platform_compute_medium``` but provide a specific usage of the machine.

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
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 240.0,
                "min": 115.5,
                "max": 522.2,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 650.0,
                "min": 565.2,
                "max": 803.5
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.036,
                "min": 0.0244,
                "max": 0.05329,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.00032,
                "min": 0.0002802,
                "max": 0.0003983
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 3200.0,
                "min": 1535.0,
                "max": 6773.0,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 75000.0,
                "min": 65110.0,
                "max": 92560.0
            }
        }
    },
    "verbose": {
        "duration": {
            "value": 8760.0,
            "unit": "hours"
        },
        "ASSEMBLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 1.67,
                        "min": 1.67,
                        "max": 1.67,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 3.525e-07,
                        "min": 3.525e-07,
                        "max": 3.525e-07,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 17.15,
                        "min": 17.15,
                        "max": 17.15,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CPU-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 10.0,
                        "min": 5.459,
                        "max": 40.91,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 848.4,
                        "min": 848.4,
                        "max": 848.4
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0102,
                        "min": 0.0102,
                        "max": 0.01021,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 0.0004206,
                        "min": 0.0004206,
                        "max": 0.0004206
                    }
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 150.0,
                        "min": 89.96,
                        "max": 566.8,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 97730.0,
                        "min": 97730.0,
                        "max": 97730.0
                    }
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
                "max": 2.0
            },
            "die_size": {
                "value": 521.0,
                "status": "COMPLETED",
                "unit": "mm2",
                "source": "Average value for all families",
                "min": 41.2,
                "max": 3640.0
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 494.12,
                "status": "COMPLETED",
                "unit": "W",
                "min": 494.12,
                "max": 494.12
            },
            "time_workload": {
                "value": 90.0,
                "status": "INPUT",
                "unit": "%"
            },
            "usage_location": {
                "value": "FRA",
                "status": "INPUT",
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
                "value": 0.098,
                "status": "COMPLETED",
                "unit": "kg CO2eq/kWh",
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
                "min": 0.098,
                "max": 0.098
            },
            "adp_factor": {
                "value": 4.85798e-08,
                "status": "COMPLETED",
                "unit": "kg Sbeq/kWh",
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 4.85798e-08,
                "max": 4.85798e-08
            },
            "pe_factor": {
                "value": 11.289,
                "status": "COMPLETED",
                "unit": "MJ/kWh",
                "source": "ADPf / (1-%renewable_energy)",
                "min": 11.289,
                "max": 11.289
            }
        },
        "RAM-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 120.0,
                        "min": 52.29,
                        "max": 294.7,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 500.0,
                        "min": 280.9,
                        "max": 780.2
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0066,
                        "min": 0.003808,
                        "max": 0.01229,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 0.00025,
                        "min": 0.0001392,
                        "max": 0.0003867
                    }
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 1600.0,
                        "min": 662.7,
                        "max": 3679.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 58000.0,
                        "min": 32350.0,
                        "max": 89870.0
                    }
                }
            },
            "units": {
                "value": 8.0,
                "status": "ARCHETYPE",
                "min": 6.0,
                "max": 10.0
            },
            "capacity": {
                "value": 32.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 32.0,
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
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 72.704,
                "status": "COMPLETED",
                "unit": "W",
                "min": 54.52799999999999,
                "max": 90.88
            },
            "time_workload": {
                "value": 90.0,
                "status": "INPUT",
                "unit": "%"
            },
            "usage_location": {
                "value": "FRA",
                "status": "INPUT",
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
                    "a": 9.088
                },
                "status": "COMPLETED",
                "source": "(ram_electrical_factor_per_go : 0.284) * (ram_capacity: 32.0) "
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
                "value": 4.85798e-08,
                "status": "COMPLETED",
                "unit": "kg Sbeq/kWh",
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 4.85798e-08,
                "max": 4.85798e-08
            },
            "pe_factor": {
                "value": 11.289,
                "status": "COMPLETED",
                "unit": "MJ/kWh",
                "source": "ADPf / (1-%renewable_energy)",
                "min": 11.289,
                "max": 11.289
            }
        },
        "SSD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 12.0,
                        "min": 5.882,
                        "max": 70.24,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0004,
                        "min": 0.0002638,
                        "max": 0.002202,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 140.0,
                        "min": 72.55,
                        "max": 870.8,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "min": 1.0,
                "max": 2.0
            },
            "capacity": {
                "value": 1000.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 1000.0,
                "max": 1000.0
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "POWER_SUPPLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 36.0,
                        "min": 12.15,
                        "max": 60.75,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.012,
                        "min": 0.00415,
                        "max": 0.02075,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 530.0,
                        "min": 176.0,
                        "max": 880.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CASE-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 38.0,
                        "min": 21.48,
                        "max": 37.5,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.005,
                        "min": 0.00505,
                        "max": 0.006918,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 550.0,
                        "min": 307.2,
                        "max": 550.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
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
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "MOTHERBOARD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 16.52,
                        "min": 16.52,
                        "max": 16.52,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.0009225,
                        "min": 0.0009225,
                        "max": 0.0009225,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "pe": {
                    "unit": "MJ",
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "value": 209.0,
                        "min": 209.0,
                        "max": 209.0,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "avg_power": {
            "value": 753.87592,
            "status": "COMPLETED",
            "unit": "W",
            "min": 658.3776,
            "max": 936.0
        },
        "time_workload": {
            "value": 90.0,
            "status": "INPUT",
            "unit": "%"
        },
        "usage_location": {
            "value": "FRA",
            "status": "INPUT",
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
            "value": 4.85798e-08,
            "status": "COMPLETED",
            "unit": "kg Sbeq/kWh",
            "source": "ADEME Base IMPACTS \u00ae",
            "min": 4.85798e-08,
            "max": 4.85798e-08
        },
        "pe_factor": {
            "value": 11.289,
            "status": "COMPLETED",
            "unit": "MJ/kWh",
            "source": "ADPf / (1-%renewable_energy)",
            "min": 11.289,
            "max": 11.289
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

</details>

* The API will create a consumption profile based on the default characteristics and apply it for an average level of workload of 90%
* The server impacts are assessed for a usage of 1 year (since duration is set at 8785 hours).
* Embedded impacts will be allocated on 1 year (since duration is set at 8785 hours).



For further information see : [The explanation page on servers](../Explanations/devices/server.md)