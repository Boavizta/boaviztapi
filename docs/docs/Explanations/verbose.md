# Verbose

Each route returning impacts can also return a verbose object if query parameter ```verbose = true```. This object describes :

1 - The impacts of each of the components *(in case of devices)*

```json
  "impacts": {
    "gwp": X,
    "pe": Y,
    "adp": Z
  }
 
```

2 - For each of the attributes the value sent by the user (```input_value```), the value used (```used_value```) and the status of the value (```status```). Three cases :
    
* **SET** : The user sent no value, a value was set
    
```json
"attribute" : {
  "input_value": null,
  "used_value": value,
  "status": "SET"
}
```

* **UNCHANGED** : The user sent a value, the value wasn't modify
  
```json
"attribute" : {
  "input_value": value,
  "used_value": value,
  "status": "UNCHANGED"
}
```
  
* **CHANGED**: The user sent a value, the value was modified
  
```json
"attribute" : {
  "input_value": value1,
  "used_value": value2,
  "status": "CHANGED"
}
```

## Example

**Input**
```json
{
  "model": {
    "manufacturer": "Dell",
    "name": "R740",
    "type": "rack",
    "year": 2020,
    "archetype": "dellR740"
  },
  "configuration": {
    "cpu": {
      "units": 2
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
        "units": 1,
        "type": "ssd"
      }
    ],
    "power_supply": {
      "units": 2
    }
  }
}
```


**Verbose**
```json
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
          "value": 650,
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
          "value": 2100,
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
          "value": 836,
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
          "value": 0.00000141,
          "unit": "kgSbeq"
        }
      }
    },
    "USAGE-1": {
      "unit": 1,
      "hash": 0,
      "years_use_time": {
        "input_value": 1,
        "used_value": 1,
        "status": "UNCHANGED"
      },
      "days_use_time": {
        "input_value": 1,
        "used_value": 1,
        "status": "UNCHANGED"
      },
      "hours_use_time": {
        "input_value": 1,
        "used_value": 1,
        "status": "UNCHANGED"
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
        "used_value": 6.42e-8,
        "status": "SET"
      },
      "max_power": {
        "input_value": 510,
        "used_value": 510,
        "status": "UNCHANGED"
      },
      "workload": {
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
        "100": {
          "time": {
            "input_value": 0.15,
            "used_value": 0.15,
            "status": "UNCHANGED"
          },
          "power": {
            "input_value": 1,
            "used_value": 1,
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
          "value": 1170,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 39800,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.000198,
          "unit": "kgSbeq"
        }
      }
    }
  }
```