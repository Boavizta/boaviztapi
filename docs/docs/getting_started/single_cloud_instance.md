# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of cloud instance (AWS use case).

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'http://localhost:5000/v1/component/cpu' | jq`)_

## Get the impacts from cpu name

This query return the list of available aws instances 

Query: 
```bash
# Query the available aws instances
curl -X 'GET' \
  'https://api.boavizta.org/v1/cloud/aws/all_instances' \
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

* The usage impact of 1 year of compute at 50% of load for a ```r6g.medium``` instance type in europe
* The total manufacture impacts of a ```r6g.medium```

Query:

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'POST' \
  'https://api.boavizta.org/v1/cloud/aws?instance_type=r6g.medium&verbose=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Results:
```json
{
  "gwp": {
    "manufacture": 36.0,
    "use": 18.0,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 460.0,
    "use": 610.0,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.0027,
    "use": 3.1e-06,
    "unit": "kgSbeq"
  }
}

```

## Get the values used to measure the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components (including usage) and the value of the attributes used for the calculation.

Query :

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'POST' \
  'https://api.boavizta.org/v1/cloud/aws?instance_type=r6g.medium&verbose=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Response :

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 36.0,
      "use": 18.0,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 460.0,
      "use": 610.0,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.0027,
      "use": 3.1e-06,
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "CPU-1": {
      "unit": 1,
      "hash": "8c8e46192c3d81601f833f27788b714ff684b227b31246d6a6335681a9693d87",
      "core_units": {
        "input_value": null,
        "used_value": 24,
        "status": "SET"
      },
      "die_size_per_core": {
        "input_value": null,
        "used_value": 0.245,
        "status": "SET"
      },
      "process": {
        "input_value": null,
        "used_value": 7.0,
        "status": "SET"
      },
      "manufacturer": {
        "input_value": null,
        "used_value": "Annapurna Labs",
        "status": "SET"
      },
      "manufacture_date": {
        "input_value": null,
        "used_value": "2019",
        "status": "SET"
      },
      "family": {
        "input_value": null,
        "used_value": "Graviton2",
        "status": "SET"
      },
      "impacts": {
        "gwp": {
          "value": 21.7,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 325.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.02,
          "unit": "kgSbeq"
        }
      }
    },
    "RAM-1": {
      "unit": 16,
      "hash": "a34b138e4ee0b4c832576fe84c3ef50c4e9713ab83fe8269fdc4dbacfd382efb",
      "capacity": {
        "input_value": null,
        "used_value": 32,
        "status": "SET"
      },
      "density": {
        "input_value": null,
        "used_value": 0.625,
        "status": "SET"
      },
      "impacts": {
        "gwp": {
          "value": 1920.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 24000.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0784,
          "unit": "kgSbeq"
        }
      }
    },
    "POWER_SUPPLY-1": {
      "unit": 2,
      "hash": "be84aabaaac41126e1bd93ec3c10b355c6c7534cf9e3d7337cef9d6d0bb116c6",
      "unit_weight": {
        "input_value": null,
        "used_value": 2.99,
        "status": "SET"
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
        "input_value": null,
        "used_value": "rack",
        "status": "SET"
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
    "SSD-1": {
      "unit": 1,
      "hash": "cb269039943b145f924c394acd2f665c10b23bddf954428af81bd8eccaff3d6a",
      "capacity": {
        "input_value": null,
        "used_value": 1000,
        "status": "SET"
      },
      "density": {
        "input_value": null,
        "used_value": 48.5,
        "status": "SET"
      },
      "impacts": {
        "gwp": {
          "value": 52.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 640.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0019,
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
        "used_value": 0.3478858,
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
        "input_value": null,
        "used_value": 489.98,
        "status": "SET"
      },
      "workload": {
        "idle": {
          "power": {
            "input_value": null,
            "used_value": 0.31,
            "status": "SET"
          },
          "time": {
            "input_value": null,
            "used_value": 0.0,
            "status": "SET"
          }
        },
        "10": {
          "power": {
            "input_value": null,
            "used_value": 0.47,
            "status": "SET"
          },
          "time": {
            "input_value": null,
            "used_value": 0.0,
            "status": "SET"
          }
        },
        "50": {
          "power": {
            "input_value": null,
            "used_value": 0.71,
            "status": "SET"
          },
          "time": {
            "input_value": null,
            "used_value": 1.0,
            "status": "SET"
          }
        },
        "100": {
          "power": {
            "input_value": null,
            "used_value": 1.0,
            "status": "SET"
          },
          "time": {
            "input_value": null,
            "used_value": 0.0,
            "status": "SET"
          }
        }
      },
      "instance_per_server": {
        "input_value": null,
        "used_value": 64.0,
        "status": "SET"
      },
      "impacts": {
        "gwp": {
          "value": 1160.0,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 39200.0,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000196,
          "unit": "kgSbeq"
        }
      }
    }
  }
}
```

## Get the impacts of a cloud instance with custom usage data

In this query you override default usage data with your custom data for ```r6g.medium``` instance type

*Notes: you can override zero to many attributes.*

Query:

```bash
# Query the data for `r6g.medium` with custom usage value
curl -X 'POST' \
  'https://api.boavizta.org/v1/cloud/aws?instance_type=r6g.medium&verbose=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "hours_use_time": 2,
  "usage_location": "FRA",
  "workload": {
    "10": {
      "time": 0
    },
    "50": {
      "time": 0.5
    },
    "100": {
      "time": 0
    },
    "idle": {
      "time": 0.5
    }
  }
}'
```

the query usage can be translated as such :

```I used a r6g.medium in a french datacenter for 2 hours half of the time in IDLE mode and half of the time at 50% of workload```

Results:

```json
{
  "gwp": {
    "manufacture": 36.0,
    "use": 0.00077,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 460.0,
    "use": 0.088,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.0027,
    "use": 3.8e-10,
    "unit": "kgSbeq"
  }
}
```