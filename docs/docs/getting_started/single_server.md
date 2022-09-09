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
"gwp": {
    "manufacture": 970,
    "use": 1000,
    "unit": "kgCO2eq"
  },
"pe": {
    "manufacture": 13000,
    "use": 33800,
    "unit": "MJ"
  },
"adp": {
    "manufacture": 0.15,
    "use": 0.000169,
    "unit": "kgSbeq"
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

- The impacts (gwp, pe, adp) at the server level (global cumulated impacts)
- The impacts of manufacturing (gwp, pe, adp) for each component (like RAM, CPU, SSD a.s.o)
- The impacts device usage
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```JSON
{
  "impacts": {
    "gwp": {
      "manufacture": 970,
      "use": 1000,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 13000,
      "use": 33800,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.15,
      "use": 0.000169,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "ASSEMBLY-1": {
      "units": 1,
      "impacts": {
        "gwp": {
          "value": 6.68,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 68.6,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.00000141,
          "unit": "kgSbeq"
        }
      }
    },
    "CPU-1": {
      "units": 2,
      "impacts": {
        "gwp": {
          "value": 43.4,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 650,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.04,
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
      }
    },
    "RAM-1": {
      "units": 12,
      "impacts": {
        "gwp": {
          "value": 540,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 6720,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0336,
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
      }
    },
    "SSD-1": {
      "units": 1,
      "impacts": {
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
      "impacts": {
        "gwp": {
          "value": 145.4,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 2100,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.05,
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
      "impacts": {
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
      "impacts": {
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
      "hours_electrical_consumption": {
        "value": 300,
        "unit": "W",
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
        "value": 6.42e-8,
        "unit": "kgCO2e/kWh",
        "status": "COMPLETED",
        "source": "ADEME BASE IMPACT"
      },
      "gwp_factor": {
        "value": 0.38,
        "unit": "KgSbeq/kWh",
        "status": "COMPLETED",
        "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries"
      },
      "pe_factor": {
        "value": 12.874,
        "unit": "MJ/kWh",
        "status": "COMPLETED",
        "source": "ADPf / (1-%renewable_energy)"
        }
      },
      "use_time": {
        "value": 8760,
        "unit": "hours",
        "status": "DEFAULT",
        "source": null
      },
      "impacts": {
        "gwp": {
          "value": 1000,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 33800,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000169,
          "unit": "kgSbeq"
        }
      }
    }
  }
}
```

## Retrieve the impacts of a _custom_ server

In this query, you refer to a _standard_ server, but provide a specific configuration of the machine (like extra RAM).

The API returns impacts, updated to reflect your _own_ server configuration.

Query : 

```bash
curl -X 'POST' \
  'https://api.boavizta.org/v1/server/?verbose=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": {
    "type": "rack",
    "archetype": "dellR740"
  },
  "configuration": {
    "cpu": {
      "units": 2,
      "core_units": 24,
      "die_size_per_core": 0.245
    },
    "ram": [
      {
        "units": 12,
        "capacity": 32,
        "density": 1.79
      }
    ],
    "disk": [
      {
        "units": 2,
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

* A server is sent with a custom [configuration](../Reference/configuration.md)
* A default [usage](../Reference/usage.md) is used _(1 hour of usage at 300 Watt of power in E urope)_

* ```"archetype": "dellR740"``` will replace all missing value with values from Boavizta's database dellR740

Result :

```json
{
    "gwp": {
      "manufacture": 990,
      "use": 1000,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 13000,
      "use": 33800,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.15,
      "use": 0.000169,
      "unit": "kgSbeq"
    }
}
```

## Retrieve the impacts with a _custom_ usage

In this query, we use the default server configuration, but provide a specific usage of the machine.

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
        "value": 4.86e-8,
        "unit": "kgCO2e/kWh",
        "status": "COMPLETED",
        "source": {
          "43": "ADEME BASE IMPACT"
        }
      },
      "gwp_factor": {
        "value": 0.098,
        "unit": "KgSbeq/kWh",
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
      "impacts": {
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
      }
    }
  }
}
```