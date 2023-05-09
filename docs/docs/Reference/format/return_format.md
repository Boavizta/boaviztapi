## Impact formats

The API returns the impacts in a JSON dictionary format. The impacts are returned in the following format:

```json
 "impacts": {
    "gwp": {
      "other": {
        "value": 64.7,
        "significant_figures": 3,
        "min": 12.3,
        "max": 298
      },
      "use": {
        "value": 1200,
        "significant_figures": 2,
        "min": 37,
        "max": 5700
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp":{...},
    ...
}
```

## Verbose

If verbose is set to true, the response will contain more information about the impacts. In the case of a device, the impacts for each component will be returned.

```json
"verbose": {
    "ASSEMBLY-1": {...},
    "CPU-1": {
      "impacts": {
        "gwp": {
          "other": {
            "value": 64.7,
            "significant_figures": 3,
            "min": 12.3,
            "max": 298
          },
          "use": {
            "value": 1200,
            "significant_figures": 2,
            "min": 37,
            "max": 5700
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        },
        "adp": {
          "other": {
            "value": 0.041,
            "significant_figures": 2,
            "min": 0.02,
            "max": 0.082
          },
          "use": {
            "value": 0.000205,
            "significant_figures": 3,
            "min": 0.0000211,
            "max": 0.0017
          },
          "unit": "kgSbeq",
          "description": "Use of minerals and fossil ressources"
        },
        "pe": {
          "other": {
            "value": 937,
            "significant_figures": 3,
            "min": 199,
            "max": 4140
          },
          "use": {
            "value": 41100,
            "significant_figures": 4,
            "min": 20.75,
            "max": 2989000
          },
          "unit": "MJ",
          "description": "Consumption of primary energy"
        }
      },
      "die_size_per_core": {
        "value": 0.47078947368421054,
        "status": "COMPLETED",
        "unit": "mm2",
        "source": "Average for all families",
        "min": 0.07,
        "max": 1.02
      },
     ...},
    "RAM-1": {...},
    "SSD-1": {...},
    "POWER_SUPPLY-1": {...},
    "CASE-1": {...},
    "MOTHERBOARD-1": {...}
    
  }
```

### Boattributes

In addition to the impacts, the response will contain the boattributes of the components. The boattributes are the attributes that are used to calculate the impacts. They contain the value, the error margin (in the form of min & max values), the unit, the status and the source of the value.

```json
"die_size_per_core": {
  "value": 0.47078947368421054,
  "status": "COMPLETED",
  "unit": "mm2",
  "source": "Average for all families",
  "min": 0.07,
  "max": 1.02
},
```