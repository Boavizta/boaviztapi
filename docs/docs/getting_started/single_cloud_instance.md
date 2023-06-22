# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of cloud instance (AWS use case).

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'http://localhost:5000/v1/cloud/aws?instance_type=a1.xlarge' | jq`)_

## Get the impacts from cpu name

This query return the list of available aws instances 

Query: 
```bash
# Query the available aws instances
curl -X 'GET' \
  'https://api.boavizta.org/v1/cloud/all_instances?cloud_provider=aws' \
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
* The **total manufacture impacts** of a ```r6g.medium```

Query:

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  'https://api.boavizta.org/v1/cloud/?cloud_provider=aws&instance_type=r6g.medium&verbose=false' \
  -H 'accept: application/json'
```

Results:
```json
{
  "gwp": {
    "manufacture": 36,
    "use": 21,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 450,
    "use": 709,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.0027,
    "use": 3.54e-06,
    "unit": "kgSbeq"
  }
}
```

## Get the values used to measure the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its components (including usage) and the value of the attributes used for the calculation.

Query :

```bash
# Query the data for `r6g.medium` with default usage value
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  'https://api.boavizta.org/v1/cloud/?cloud_provider=aws&instance_type=r6g.medium&verbose=true' \
  -H 'accept: application/json'
```

Response :

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 36,
      "use": 21,
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 450,
      "use": 709,
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.0027,
      "use": 3.54e-06,
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
      "units": 1,
      "manufacture_impacts": {
        "gwp": {
          "value": 19.1,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 290,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.02,
          "unit": "kgSbeq"
        }
      },
      "core_units": {
        "value": 64,
        "unit": "none",
        "status": "INPUT",
        "source": null
      },
      "die_size_per_core": {
        "value": 0.0714,
        "unit": "cm2",
        "status": "COMPLETED",
        "source": {
          "64": "https://en.wikichip.org/wiki/annapurna_labs/alpine/alc12b00"
        }
      },
      "family": {
        "value": "graviton2",
        "unit": "none",
        "status": "CHANGED",
        "source": null
      },
      "tdp": {
        "value": 210,
        "unit": "W",
        "status": "INPUT",
        "source": null
      },
      "USAGE": {
        "usage_impacts": {
          "gwp": {
            "value": 520,
            "unit": "kgCO2eq"
          },
          "pe": {
            "value": 17720,
            "unit": "MJ"
          },
          "adp": {
            "value": 8.84e-05,
            "unit": "kgSbeq"
          }
        },
        "hours_electrical_consumption": {
          "value": 157.11830305304008,
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
        "workloads": {
          "value": [
            {
              "load_percentage": 0,
              "power_watt": 25.2
            },
            {
              "load_percentage": 10,
              "power_watt": 67.2
            },
            {
              "load_percentage": 50,
              "power_watt": 157.5
            },
            {
              "load_percentage": 100,
              "power_watt": 214.20000000000002
            }
          ],
          "unit": "workload_rate:W",
          "status": "COMPLETED",
          "source": null
        },
        "params": {
          "value": {
            "a": 106.7806614802558,
            "b": 0.06385367477645258,
            "c": 20.45110317833163,
            "d": -3.4539444500465573
          },
          "unit": "none",
          "status": "COMPLETED",
          "source": "From TDP"
        }
      }
    },
    "RAM-1": {
      "units": 16,
      "manufacture_impacts": {
        "gwp": {
          "value": 120,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 1500,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.0049,
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
        "value": 0.625,
        "unit": "GB/cm2",
        "status": "DEFAULT",
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
        "status": "DEFAULT",
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
          "value": 21,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 709,
          "unit": "MJ"
        },
        "adp": {
          "value": 3.54e-06,
          "unit": "kgSbeq"
        }
      },
      "hours_electrical_consumption": {
        "value": 402.3599830605433,
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
      },
      "instance_per_server": {
        "value": 64,
        "unit": "none",
        "status": "INPUT",
        "source": null
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
  'https://api.boavizta.org/v1/cloud/?verbose=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": "aws",
    "instance_type": "r6g.medium",
    "usage": {
       "hours_use_time": 2,
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

the query usage can be translated as such :

```I used a r6g.medium in a french data center for 2 hours half of the time in IDLE mode and half of the time at 50% of workload```

Results:

```json
{
  "gwp": {
    "manufacture": 36,
    "use": 0.0009,
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 450,
    "use": 0.1,
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.0027,
    "use": 4e-10,
    "unit": "kgSbeq"
  }
}
```

For further information see : [The explanation page on cloud](../Explanations/devices/cloud.md)
