# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of terminal and peripherals.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws?instance_type=a1.xlarge' | jq`)_

## Get the impacts of a laptop with a default usage

In this query, we compute the impact of a laptop

Query : 

```bash
curl -X 'GET' \
  '{{ endpoint }}/v1/terminal/laptop?verbose=false' \
  -H 'accept: application/json'
```

This query returns :

- The impacts for the default criteria (gwp, pe, adp) since no impact is specified
- The total embedded impacts of the laptop since no duration is given
- The usage impacts of the laptop during its life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Significant figures are provided for each value

Result :

```json
{
  "gwp": {
    "embedded": {
      "value": 181,
      "significant_figures": 3,
      "min": 181,
      "max": 181,
      "warnings": [
        "Generic data used for impact calculation."
      ]
    },
    "use": {
      "value": 299.59,
      "significant_figures": 5,
      "min": 12.089,
      "max": 1189.5
    },
    "unit": "kgCO2eq",
    "description": "Total climate change"
  },
  "adp": {
    "embedded": "not implemented",
    "use": {
      "value": 5.064e-05,
      "significant_figures": 5,
      "min": 6.9589e-06,
      "max": 0.00027917
    },
    "unit": "kgSbeq",
    "description": "Use of minerals and fossil ressources"
  },
  "pe": {
    "embedded": "not implemented",
    "use": {
      "value": 10149,
      "significant_figures": 5,
      "min": 6.8328,
      "max": 492120
    },
    "unit": "MJ",
    "description": "Consumption of primary energy"
  }
}
```

## Get the impact of a desktop with a custom usage

In this query, we compute the impact of a desktop with a custom usage. Since ```verbose=true``` the api will return the values used during the computation.
 
```bash
curl -X 'POST' \
  'http://localhost:5000/v1/terminal/desktop?verbose=true&duration=8760&criteria=gwp&criteria=adp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "usage": {
    "avg_power":70,
    "use_time_ratio":0.3,
    "usage_location": "FRA"
  }
}'
```

This query returns :

* The impacts for both gwp and adp criteria since ```criteria=gwp&criteria=adp```
* The API will use an average electrical consumption of 70 Watt/hours 30% of the time (since ```use_time_ratio=0.3```) for one year (since duration is set at 8760 hours). 
* Usage impacts will be assessed for the French electrical mix impacts since ```usage_location='FRA'```
* Embedded impacts will be allocated on one year (since duration is set at 8760 hours).

```json
{
  "impacts": {
    "gwp": {
      "embedded": {
        "value": 46.2,
        "significant_figures": 3,
        "min": 46.2,
        "max": 46.2,
        "warnings": [
          "Generic data used for impact calculation."
        ]
      },
      "use": {
        "value": 18.028,
        "significant_figures": 5,
        "min": 18.028,
        "max": 18.028
      },
      "unit": "kgCO2eq",
      "description": "Total climate change"
    },
    "adp": {
      "embedded": "not implemented",
      "use": {
        "value": 8.9367e-06,
        "significant_figures": 5,
        "min": 8.9367e-06,
        "max": 8.9367e-06
      },
      "unit": "kgSbeq",
      "description": "Use of minerals and fossil ressources"
    }
  },
  "verbose": {
    "duration": {
      "value": 8760,
      "unit": "hours"
    },
    "avg_power": {
      "value": 70,
      "status": "INPUT",
      "unit": "W"
    },
    "usage_location": {
      "value": "FRA",
      "status": "INPUT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    },
    "use_time_ratio": {
      "value": 0.3,
      "status": "INPUT",
      "unit": "/1"
    },
    "hours_life_time": {
      "value": 52560,
      "status": "ARCHETYPE",
      "unit": "hours",
      "min": 52560,
      "max": 52560
    },
    "gwp_factor": {
      "value": 0.098,
      "status": "COMPLETED",
      "unit": "kg CO2eq/kWh",
      "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
      "min": 0.098,
      "max": 0.098
    },
    "adp_factor": {
      "value": 4.85798e-08,
      "status": "COMPLETED",
      "unit": "kg Sbeq/kWh",
      "source": "ADEME Base IMPACTS ®",
      "min": 4.85798e-08,
      "max": 4.85798e-08
    },
    "units": {
      "value": 1,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 1
    },
    "type": {
      "value": "pro",
      "status": "ARCHETYPE"
    }
  }
}
```
For further information see : [The explanation page on terminal and peripherals](../Explanations/devices/terminals_&_peripherals.md)