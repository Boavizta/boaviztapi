# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'https://api.boavizta.org/v1/server/model?archetype=dellR740' | jq`)_

## Get the impacts of a dellR740 server

This is the simplest possible query. It returns the impacts of a _standard_ (i.e. predefined) server configuration (dellR740).

Query: 
```bash
# Query the data for `dellR740`
curl -X 'GET' \
  'https://api.boavizta.org/v1/server/model?archetype=dellR740&verbose=false' \
  -H 'accept: application/json'
```

Results:

```json
{
  "gwp": {
    "manufacture": 970,
    "use": 2100,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 13000,
    "use": 71020,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.15,
    "use": 0.000354,
    "unit": "kgSbeq"
  }
}
```

## Get the values used to measure the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components and the value of the attributes used for the calculation.

Query:

```bash
# Query the data for `dellR740`
curl -X 'GET' \
  'https://api.boavizta.org/v1/server/model?archetype=dellR740&verbose=true' \
  -H 'accept: application/json'
```

It returns :

- The total impacts of manufacturing (gwp, pe, adp) for each component (like RAM, CPU, SSD a.s.o)
- The impacts (gwp, pe, adp) of usage at server level for one year
- The impacts (gwp, pe, adp) of usage for CPU and RAM for one year
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```JSON
{
  "impacts": {
    "gwp": {
      "manufacture": 970,
      "use": 2100,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 13000,
      "use": 71020,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.15,
      "use": 0.000354,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "ASSEMBLY-1": {
      "units": 1,
      "manufacture_impacts": {
        "gwp": {
          "value": 6.68,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 68.6,
          "unit": "MJ"
        },
        "adp": {
          "value": 1.41e-06,
          "unit": "kgSbeq"
        }
      }
    },
    "CPU-1": {
      "units": 2,
      "manufacture_impacts": {
        "gwp": {
          "value": 21.7,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 325,
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
        "value": 0.245,
        "unit": "mm2",
        "status": "INPUT",
        "source": null
      },
      "USAGE": {
        "usage_impacts": {
          "gwp": {
            "value": 610,
            "unit": "kgCO2eq"
          },
          "pe": {
            "value": 20550,
            "unit": "MJ"
          },
          "adp": {
            "value": 0.000102,
            "unit": "kgSbeq"
          }
        },
        "hours_electrical_consumption": {
          "value": 182.23023303189055,
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
            "a": 171.2,
            "b": 0.0354,
            "c": 36.89,
            "d": -10.13
          },
          "unit": "none",
          "status": "DEFAULT",
          "source": null
        }
      }
    },
    "RAM-1": {
      "units": 12,
      "manufacture_impacts": {
        "gwp": {
          "value": 45,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 560,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0028,
          "unit": "kgSbeq"
        }
      },
      "capacity": {
        "value": 32,
        "unit": "GB",
        "status": "INPUT",
        "source": null
      },
      "density": {
        "value": 1.79,
        "unit": "GB/cm2",
        "status": "INPUT",
        "source": null
      },
      "USAGE": {
        "usage_impacts": {
          "gwp": {
            "value": 30,
            "unit": "kgCO2eq"
          },
          "pe": {
            "value": 1025,
            "unit": "MJ"
          },
          "adp": {
            "value": 5.11e-06,
            "unit": "kgSbeq"
          }
        },
        "hours_electrical_consumption": {
          "value": 9.088,
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
            "a": 9.088
          },
          "unit": "none",
          "status": "COMPLETED",
          "source": "(ram_electrical_factor_per_go : 0.284) * (ram_electrical_factor_per_go: 32) "
        }
      }
    },
    "SSD-1": {
      "units": 1,
      "manufacture_impacts": {
        "gwp": {
          "value": 24,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 293,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0011,
          "unit": "kgSbeq"
        }
      },
      "capacity": {
        "value": 400,
        "unit": "GB",
        "status": "INPUT",
        "source": null
      },
      "density": {
        "value": 50.6,
        "unit": "GB/cm2",
        "status": "INPUT",
        "source": null
      }
    },
    "POWER_SUPPLY-1": {
      "units": 2,
      "manufacture_impacts": {
        "gwp": {
          "value": 72.7,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 1050,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.025,
          "unit": "kgSbeq"
        }
      },
      "unit_weight": {
        "value": 2.99,
        "unit": "kg",
        "status": "INPUT",
        "source": null
      }
    },
    "CASE-1": {
      "units": 1,
      "manufacture_impacts": {
        "gwp": {
          "value": 150,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 2200,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0202,
          "unit": "kgSbeq"
        }
      },
      "case_type": {
        "value": "rack",
        "unit": "none",
        "status": "INPUT",
        "source": null
      }
    },
    "MOTHERBOARD-1": {
      "units": 1,
      "manufacture_impacts": {
        "gwp": {
          "value": 66.1,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 836,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.00369,
          "unit": "kgSbeq"
        }
      }
    },
    "USAGE": {
      "usage_impacts": {
        "gwp": {
          "value": 2100,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 71020,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000354,
          "unit": "kgSbeq"
        }
      },
      "hours_electrical_consumption": {
        "value": 629.7768998648289,
        "unit": "W",
        "status": "COMPLETED",
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
      "other_consumption_ratio": {
        "value": 0.33,
        "unit": "ratio /1",
        "status": "DEFAULT",
        "source": null
      }
    }
  }
}
```

## Retrieve the impacts of a _custom_ server

In this query, you provide a specific configuration of the machine. Missing attributes or component will be replaced by default ones.

The API returns impacts, to reflect your _own_ server configuration.

Query : 

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/server/?verbose=false' \
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
    "manufacture": 1500,
    "use": 2600,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 19000,
    "use": 87380,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.17,
    "use": 0.000436,
    "unit": "kgSbeq"
  }
}
```

## Retrieve the impacts with from a custom power consumption

In this query, we use the default server configuration, but provide a specific usage of the machine.

In this specific case the average power consumption of the machine is known (```hours_electrical_consumptions``)

The API returns impacts, updated to reflect your own server usage.

Query : 

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/server/?verbose=true' \
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
     "hours_electrical_consumption": 250
    }
  }'
```

* The server is evaluated with the specific impacts of the French electrical grid.
* The server is evaluated for a usage of 1 year, 1 day, 1 hour. It corresponds to 8785 hours.
* The average electrical consumption per hour is 250 W/hour

Result :

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 3300,
      "use": 220,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 42000,
      "use": 24800,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.23,
      "use": 0.000107,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
   ...
    "USAGE": {
      "usage_impacts": {
        "gwp": {
          "value": 220,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 24800,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000107,
          "unit": "kgSbeq"
        }
      },
      "hours_electrical_consumption": {
        "value": 250,
        "unit": "W",
        "status": "INPUT",
        "source": null
      },
      "usage_location": {
        "value": "FRA",
        "unit": "CodSP3 - NCS Country Codes - NATO",
        "status": "INPUT",
        "source": null
      },
      "adp_factor": {
        "value": 4.86e-08,
        "unit": "KgSbeq/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "ADEME BASE IMPACT"
        }
      },
      "gwp_factor": {
        "value": 0.098,
        "unit": "kgCO2e/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "https://www.sciencedirect.com/science/article/pii/S0306261921012149"
        }
      },
      "pe_factor": {
        "value": 11.289,
        "unit": "MJ/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "ADPf / (1-%renewable_energy)"
        }
      },
      "use_time": {
        "value": 8785,
        "unit": "hours",
        "status": "INPUT",
        "source": null
      }
    }
  }
}

```

## Retrieve the impacts with from a custom workload

In this query, we use the default server configuration, but provide a specific usage of the machine.

In this  case the average is unknown. We use the level of workload (```time_workload```) of the machine as a proxy for the power consumption.

Query : 
```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/server/?verbose=true' \
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
      "manufacture": 3300,
      "use": 820,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 42000,
      "use": 93940,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.23,
      "use": 0.000404,
      "unit": "kgSbeq"
    }
  },
   ...
    "CPU-1": {
      ...
      "USAGE": {
        "usage_impacts": {
          "gwp": {
            "value": 820,
            "unit": "kgCO2eq"
          },
          "pe": {
            "value": 27940,
            "unit": "MJ"
          },
          "adp": {
            "value": 0.000139,
            "unit": "kgSbeq"
          }
        },
        "hours_electrical_consumption": {
          "value": 247.0598413289702,
          "unit": "W",
          "status": "COMPLETED",
          "source": null
        },
        "time_workload": {
          "value": 90,
          "unit": "%",
          "status": "INPUT",
          "source": null
        },
        "usage_location": {
          "value": "FRA",
          "unit": "CodSP3 - NCS Country Codes - NATO",
          "status": "INPUT",
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
          "value": 8785,
          "unit": "hours",
          "status": "INPUT",
          "source": null
        },
        "params": {
          "value": {
            "a": 171.2,
            "b": 0.0354,
            "c": 36.89,
            "d": -10.13
          },
          "unit": "none",
          "status": "DEFAULT",
          "source": null
        }
      }
    },
    "RAM-1": {
      ...
      "USAGE": {
        "usage_impacts": {
          "gwp": {
            "value": 30,
            "unit": "kgCO2eq"
          },
          "pe": {
            "value": 1028,
            "unit": "MJ"
          },
          "adp": {
            "value": 5.13e-06,
            "unit": "kgSbeq"
          }
        },
        "hours_electrical_consumption": {
          "value": 9.088,
          "unit": "W",
          "status": "COMPLETED",
          "source": null
        },
        "time_workload": {
          "value": 90,
          "unit": "%",
          "status": "INPUT",
          "source": null
        },
        "usage_location": {
          "value": "FRA",
          "unit": "CodSP3 - NCS Country Codes - NATO",
          "status": "INPUT",
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
          "value": 8785,
          "unit": "hours",
          "status": "INPUT",
          "source": null
        },
        "params": {
          "value": {
            "a": 9.088
          },
          "unit": "none",
          "status": "COMPLETED",
          "source": "(ram_electrical_factor_per_go : 0.284) * (ram_electrical_factor_per_go: 32) "
        }
      }
    },
    ...
    "USAGE": {
      "usage_impacts": {
        "gwp": {
          "value": 820,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 93940,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000404,
          "unit": "kgSbeq"
        }
      },
      "hours_electrical_consumption": {
        "value": 947.2681379350607,
        "unit": "W",
        "status": "COMPLETED",
        "source": null
      },
      "time_workload": {
        "value": 90,
        "unit": "%",
        "status": "INPUT",
        "source": null
      },
      "usage_location": {
        "value": "FRA",
        "unit": "CodSP3 - NCS Country Codes - NATO",
        "status": "INPUT",
        "source": null
      },
      "adp_factor": {
        "value": 4.86e-08,
        "unit": "KgSbeq/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "ADEME BASE IMPACT"
        }
      },
      "gwp_factor": {
        "value": 0.098,
        "unit": "kgCO2e/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "https://www.sciencedirect.com/science/article/pii/S0306261921012149"
        }
      },
      "pe_factor": {
        "value": 11.289,
        "unit": "MJ/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "ADPf / (1-%renewable_energy)"
        }
      },
      "use_time": {
        "value": 8785,
        "unit": "hours",
        "status": "INPUT",
        "source": null
      },
      "other_consumption_ratio": {
        "value": 0.33,
        "unit": "ratio /1",
        "status": "DEFAULT",
        "source": null
      }
    }
  }
}
```

For further information see : [The explanation page on cloud](../Explanations/devices/server.md)