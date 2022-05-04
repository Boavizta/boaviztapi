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
  "gwp":{
    "manufacture":970.0,
    "use":1170.0,
    "unit":"kgCO2eq"
  },
  "pe":{
    "manufacture":13000.0,
    "use":39700.0,
    "unit":"MJ"
  },
  "adp":{
    "manufacture":0.15,
    "use":0.000198,
    "unit":"kgSbeq"
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

- The impacts (gwp, pe, adp) at the server level (global cumulated impacts)
- The impacts (gwp, pe, adp) for each component (like RAM, CPU, SSD a.s.o)
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```JSON
{
  "impacts": {
    "gwp": {
      "manufacture": 970.0,
      "use": 1170.0,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 13000.0,
      "use": 39700.0,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.15,
      "use": 0.000198,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "CPU-1": {
      "unit": 2,
      "hash": "5f75d18d9165b04381f24cb2130b62f756d266c45080982334585931482398ad",
      "core_units": {
        "input_value": 24,
        "used_value": 24,
        "status": "UNCHANGED"
      },
      "die_size_per_core": {
        "input_value": 0.245,
        "used_value": 0.245,
        "status": "UNCHANGED"
      },
      "impacts": {
        "gwp": {
          "value": 43.4,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 650.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.04,
          "unit": "kgSbeq"
        }
      }
    },
    "RAM-1": {
      "unit": 12,
      "hash": "4985faa0d798469b3deea291f6e9852862e43a06f5364164e57801035cfa3410",
      "capacity": {
        "input_value": 32,
        "used_value": 32,
        "status": "UNCHANGED"
      },
      "density": {
        "input_value": 1.79,
        "used_value": 1.79,
        "status": "UNCHANGED"
      },
      "impacts": {
        "gwp": {
          "value": 540.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 6720.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0336,
          "unit": "kgSbeq"
        }
      }
    },
    "SSD-1": {
      "unit": 1,
      "hash": "41514f07d8fa09207407a0693c20b7647cba1751e658999a51b4c003fc032c91",
      "capacity": {
        "input_value": 400,
        "used_value": 400,
        "status": "UNCHANGED"
      },
      "density": {
        "input_value": 50.6,
        "used_value": 50.6,
        "status": "UNCHANGED"
      },
      "impacts": {
        "gwp": {
          "value": 24.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 293.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0011,
          "unit": "kgSbeq"
        }
      }
    },
    "POWER_SUPPLY-1": {
      "unit": 2,
      "hash": "cdb1c15f77554bf77b8d8ccc2094af7ed72a8a19ff3f0fd0a9909ecacec06428",
      "unit_weight": {
        "input_value": 2.99,
        "used_value": 2.99,
        "status": "UNCHANGED"
      },
      "impacts": {
        "gwp": {
          "value": 145.32,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 2100.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0496,
          "unit": "kgSbeq"
        }
      }
    },
    "CASE-1": {
      "unit": 1,
      "hash": "083dcd17f9997756af73de7c61f0cf2986b25075ad00bbf7c07e08cc80a2183f",
      "case_type": {
        "input_value": "rack",
        "used_value": "rack",
        "status": "UNCHANGED"
      },
      "impacts": {
        "gwp": {
          "value": 150.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 2200.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0202,
          "unit": "kgSbeq"
        }
      }
    },
    "MOTHERBOARD-1": {
      "unit": 1,
      "hash": "3a31a8fbd4b871719831ef11af93eefbb1c2afc0f62d850a31fb5475aac9336e",
      "impacts": {
        "gwp": {
          "value": 66.1,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 836.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.00369,
          "unit": "kgSbeq"
        }
      }
    },
    "ASSEMBLY-1": {
      "unit": 1,
      "hash": "8bfe70a2b59691c050865455cc9cf1b561ec702e7cf930c1026a490964bbd364",
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
          "value": 1.41e-06,
          "unit": "kgSbeq"
        }
      }
    },
    "USAGE-1": {
      "unit": 1,
      "hash": 0,
      "years_use_time": {
        "input_value": null,
        "used_value": 1,
        "status": "SET"
      },
      "hours_electrical_consumption": {
        "input_value": null,
        "used_value": 0.35174445000000004,
        "status": "SET"
      },
      "usage_location": {
        "input_value": null,
        "used_value": "EEE",
        "status": "SET"
      },
      "gwp_factor": {
        "input_value": null,
        "used_value": 0.38,
        "status": "SET"
      },
      "pe_factor": {
        "input_value": null,
        "used_value": 12.874,
        "status": "SET"
      },
      "adp_factor": {
        "input_value": null,
        "used_value": 6.42e-08,
        "status": "SET"
      },
      "max_power": {
        "input_value": 510.0,
        "used_value": 510.0,
        "status": "UNCHANGED"
      },
      "workload": {
        "100": {
          "time": {
            "input_value": 0.15,
            "used_value": 0.15,
            "status": "UNCHANGED"
          },
          "power": {
            "input_value": 1.0,
            "used_value": 1.0,
            "status": "UNCHANGED"
          }
        },
        "50": {
          "time": {
            "input_value": 0.55,
            "used_value": 0.55,
            "status": "UNCHANGED"
          },
          "power": {
            "input_value": 0.7235,
            "used_value": 0.7235,
            "status": "UNCHANGED"
          }
        },
        "10": {
          "time": {
            "input_value": 0.2,
            "used_value": 0.2,
            "status": "UNCHANGED"
          },
          "power": {
            "input_value": 0.5118,
            "used_value": 0.5118,
            "status": "UNCHANGED"
          }
        },
        "idle": {
          "time": {
            "input_value": 0.1,
            "used_value": 0.1,
            "status": "UNCHANGED"
          },
          "power": {
            "input_value": 0.3941,
            "used_value": 0.3941,
            "status": "UNCHANGED"
          }
        }
      },
      "impacts": {
        "gwp": {
          "value": 1170.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 39700.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000198,
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
    "manufacturer": "Dell",
    "name": "My-Dell740",
    "type": "rack",
    "year": 2020,
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
  },
  "usage": {
    "max_power": 510,
    "years_use_time": 1,
    "days_use_time": 1,
    "hours_use_time": 1,
    "workload": {
      "10": {
        "time": 0.2,
        "power": 0.5118
      },
      "50": {
        "time": 0.55,
        "power": 0.7235
      },
      "100": {
        "time": 0.15,
        "power": 1
      },
      "idle": {
        "time": 0.1,
        "power": 0.3941
      }
    }
  }
}'
```

* A server is sent with a custom [configuration](../Reference/configuration.md) and [usage](../Reference/usage.md) characteristics

* ```"archetype": "dellR740"``` will replace all missing value with values from Boavizta's database dellR740

Result :

```json
{
  "gwp": {
    "manufacture": 990.0,
    "use": 1170.0,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 13000.0,
    "use": 39800.0,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.15,
    "use": 0.000198,
    "unit": "kgSbeq"
  }
}
```