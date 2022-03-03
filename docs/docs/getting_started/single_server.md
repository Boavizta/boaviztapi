# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'http://api.boavizta.org:5000/v1/server/model?archetype=dellR740' | jq`)_

## Get the impacts of a dellR740 server

This is the simplest possible query. It returns the impacts of a _standard_ (i.e. predefined) server configuration (dellR740).

Query: 
```bash
# Query the data for `dellR740`
curl -X 'GET' \
  'http://api.boavizta.org:5000/v1/server/model?archetype=dellR740&verbose=false' \
  -H 'accept: application/json'
```

Results:

```json
{
  "gwp": {
    "manufacture": 970,
    "use": 696
  },
  "pe": {
    "manufacture": 12896,
    "use": "Not Implemented"
  },
  "adp": {
    "manufacture": 0.149,
    "use": "Not Implemented"
  }
}
```

## Get the values used to measure the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components and the value of the attributes used for the calculation.

Query:

```bash
# Query the data for `dellR740`
curl -X 'GET' \
  'http://api.boavizta.org:5000/v1/server/model?archetype=dellR740&verbose=true' \
  -H 'accept: application/json'
```

It returns :

- The impacts (gwp, pe, adp) at the server level (global cumulated impacts)
- The impacts (gwp, pe, adp) for each component (like RAM, CPU, SSD a.s.o)
- The value of the attributes used for the calculation for each component (i.e. the detailed configuration)

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 970,
      "use": 696
    },
    "pe": {
      "manufacture": 12896,
      "use": "Not Implemented"
    },
    "adp": {
      "manufacture": 0.149,
      "use": "Not Implemented"
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
        "gwp": 44,
        "pe": 650,
        "adp": 0.04
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
        "gwp": 540,
        "pe": 6744,
        "adp": 0.036
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
        "gwp": 24,
        "pe": 293,
        "adp": 0.001
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
        "gwp": 146,
        "pe": 2104,
        "adp": 0.05
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
        "gwp": 150,
        "pe": 2200,
        "adp": 0.02
      }
    },
    "MOTHERBOARD-1": {
      "unit": 1,
      "hash": "3a31a8fbd4b871719831ef11af93eefbb1c2afc0f62d850a31fb5475aac9336e",
      "impacts": {
        "gwp": 66,
        "pe": 836,
        "adp": 0.004
      }
    },
    "ASSEMBLY-1": {
      "unit": 1,
      "hash": "8bfe70a2b59691c050865455cc9cf1b561ec702e7cf930c1026a490964bbd364",
      "impacts": {
        "gwp": 7,
        "pe": 69,
        "adp": 0
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
  'http://api.boavizta.org:5000/v1/server/?verbose=true' \
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
  "impacts": {
    "gwp": {
      "manufacture": 994,
      "use": 698
    },
    "pe": {
      "manufacture": 13189,
      "use": "Not Implemented"
    },
    "adp": {
      "manufacture": 0.15,
      "use": "Not Implemented"
    }
  }
}
```