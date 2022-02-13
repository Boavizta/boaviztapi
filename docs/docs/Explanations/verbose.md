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
      "hash": "c8c7d224967280c8cb4cb95bfc1727e68645f38154310d2f8091170915f49464",
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
        "gwp": 52,
        "pe": 640,
        "adp": 0.002
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
```