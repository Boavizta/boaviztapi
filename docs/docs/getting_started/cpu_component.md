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
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 23.78,
                "min": 23.78,
                "max": 23.78,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 900.0,
                "min": 57.19,
                "max": 2814.0
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.0204,
                "min": 0.0204,
                "max": 0.0204,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.00016,
                "min": 3.292e-05,
                "max": 0.0006604
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 352.9,
                "min": 352.9,
                "max": 352.9,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 30000.0,
                "min": 32.33,
                "max": 1164000.0,
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

- The impacts for the default criteria (gwp, pe, adp) since no impact criteria is specified
- The total embedded impacts of the CPU
- The usage impacts of the CPU during the life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

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
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 23.78,
                "min": 23.78,
                "max": 23.78,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 900.0,
                "min": 57.19,
                "max": 2814.0
            }
        }
    },
    "verbose": {
        "impacts": {
            "gwp": {
                "unit": "kgCO2eq",
                "description": "Total climate change",
                "embedded": {
                    "value": 23.78,
                    "min": 23.78,
                    "max": 23.78,
                    "warnings": [
                        "End of life is not included in the calculation"
                    ]
                },
                "use": {
                    "value": 900.0,
                    "min": 57.19,
                    "max": 2814.0
                }
            },
            "adp": {
                "unit": "kgSbeq",
                "description": "Use of minerals and fossil ressources",
                "embedded": "not implemented",
                "use": "not implemented"
            },
            "pe": {
                "unit": "MJ",
                "description": "Consumption of primary energy",
                "embedded": "not implemented",
                "use": "not implemented"
            }
        },
        "units": {
            "value": 1.0,
            "status": "ARCHETYPE",
            "min": 1.0,
            "max": 1.0
        },
        "die_size": {
            "value": 694,
            "status": "COMPLETED",
            "unit": "mm2",
            "source": "Max value of cpu_manufacture https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)#Extreme_Core_Count_.28XCC.29 : Completed from name name based on https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data.",
            "min": 694,
            "max": 694
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
            "value": "Skylake",
            "status": "COMPLETED",
            "source": "Completed from name name based on https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data.",
            "min": "Skylake",
            "max": "Skylake"
        },
        "name": {
            "value": "Intel Xeon Gold 6134",
            "status": "COMPLETED",
            "source": "fuzzy match",
            "min": "Intel Xeon Gold 6134",
            "max": "Intel Xeon Gold 6134"
        },
        "duration": {
            "value": 26280.0,
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
            "value": 26280.0,
            "status": "ARCHETYPE",
            "unit": "hours",
            "min": 26280.0,
            "max": 26280.0
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

</details>

Result :

* This query will only compute the gwp (Global Warming Potential) impact since we add the `criteria=gwp` flag.
* You can see that the API has completed the needed value from the cpu name. We parse and fuzzymatch the cpu ```name``` with our dataset of cpu to identify ```tdp```, ```cores_unit```, ```family```...
* The ```die_size``` is completed from the cpu family.
* The usage impact has been assessed using a default level of workload of 50% with the consumption profile of a xeon gold (completed from cpu ```name```).


## Get the impacts from custom cpu characteristics

In this query, we give some characteristics to describe the CPU. 

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=true&criteria=gwp&criteria=adp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
 -d '{
      "core_units": 24,
      "family": "skylake"
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
                "value": 22.22,
                "min": 22.22,
                "max": 22.22,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 1800.0,
                "min": 110.1,
                "max": 5419.0
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.0204,
                "min": 0.0204,
                "max": 0.0204,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.0003,
                "min": 6.341e-05,
                "max": 0.001272
            }
        }
    },
    "verbose": {
        "impacts": {
            "gwp": {
                "unit": "kgCO2eq",
                "description": "Total climate change",
                "embedded": {
                    "value": 22.22,
                    "min": 22.22,
                    "max": 22.22,
                    "warnings": [
                        "End of life is not included in the calculation"
                    ]
                },
                "use": {
                    "value": 1800.0,
                    "min": 110.1,
                    "max": 5419.0
                }
            },
            "adp": {
                "unit": "kgSbeq",
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "value": 0.0204,
                    "min": 0.0204,
                    "max": 0.0204,
                    "warnings": [
                        "End of life is not included in the calculation"
                    ]
                },
                "use": {
                    "value": 0.0003,
                    "min": 6.341e-05,
                    "max": 0.001272
                }
            },
            "pe": {
                "unit": "MJ",
                "description": "Consumption of primary energy",
                "embedded": "not implemented",
                "use": "not implemented"
            }
        },
        "units": {
            "value": 1.0,
            "status": "ARCHETYPE",
            "min": 1.0,
            "max": 1.0
        },
        "core_units": {
            "value": 24,
            "status": "INPUT"
        },
        "die_size": {
            "value": 615.0,
            "status": "COMPLETED",
            "unit": "mm2",
            "source": "Average value of Skylake with 24 cores",
            "min": 615.0,
            "max": 615.0
        },
        "family": {
            "value": "Skylake",
            "status": "CHANGED"
        },
        "duration": {
            "value": 26280.0,
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
            "value": 26280.0,
            "status": "ARCHETYPE",
            "unit": "hours",
            "min": 26280.0,
            "max": 26280.0
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
        }
    }
}
```

</details>

* This query will compute the gwp and adp impacts since we add the `criteria=gwp&criteria=adp` flags.
* The API will correct skylake to Skylake (CHANGED) and complete the missing attributes from the given attributes (COMPLETED) or by default ones (ARCHETYPE).


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

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 0.00181,
                "min": 0.00181,
                "max": 0.00181,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.02352,
                "min": 0.02352,
                "max": 0.02352
            }
        }
    }
}
```

</details>

* The API will use an electrical power of 120 Watt for 2 hours since duration is set at 2 in query parameter
* Usage impacts will be assessed for the French electrical mix impacts since usage_location is set at FRA
* Embedded impacts will be allocated on 2 hours since duration is set at 2 in query parameter


## Get the impacts from custom cpu usage using a workload

In this query we set a custom usage to an ```intel xeon gold 6134``` with a TDP of 130 Watt. The average electrical consumption is modeled by the API.

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/component/cpu?verbose=false&criteria=gwp&duration=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "intel xeon gold 6134",
  "tdp": 130,
  "usage":{
      "usage_location": "FRA",
      "time_workload": 30
  }}'
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
                "value": 23.78,
                "min": 23.78,
                "max": 23.78,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 193.6,
                "min": 193.6,
                "max": 193.6
            }
        }
    }
}
```

</details>

* The API will use the ```xeon gold``` consumption profile adapted for a TDP of 130 Watt with a level of workload of 30% for 2 hours to retrieve the electrical consumption of the CPU.

For further information see : [The explanation page on cpu](../Explanations/components/cpu.md)