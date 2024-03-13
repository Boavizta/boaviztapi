# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of terminals and peripherals.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws?instance_type=a1.xlarge' | jq`)_

## Get the impacts of a laptop with a default usage

In this query, we compute the impacts of a laptop

Query : 

```bash
curl -X 'GET' \
  '{{ endpoint }}/v1/terminal/laptop?verbose=false' \
  -H 'accept: application/json'
```

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 181.0,
                "min": 181.0,
                "max": 181.0,
                "warnings": [
                    "Generic data used for impact calculation."
                ]
            },
            "use": "not implemented"
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": "not implemented",
            "use": "not implemented"
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": "not implemented",
            "use": "not implemented"
        }
    }
}
```

</details>

This query returns :

- The impacts for the default criteria (gwp, pe, adp) since no impact is specified
- The total embedded impacts of the laptop since no duration is given
- The usage impacts of the laptop during its life duration, since no duration is given
- Error margins are provided in the form of min & max values for both embedded and usage impacts
- Some values are not implemented, meaning that the API does not provide these impacts for this device.


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
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 277.0,
                "min": 277.0,
                "max": 277.0,
                "warnings": [
                    "Generic data used for impact calculation."
                ]
            },
            "use": {
                "value": 18.03,
                "min": 18.03,
                "max": 18.03
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": "not implemented",
            "use": {
                "value": 8.937e-06,
                "min": 8.937e-06,
                "max": 8.937e-06
            }
        }
    },
    "verbose": {
        "duration": {
            "value": 8760.0,
            "unit": "hours"
        },
        "avg_power": {
            "value": 70.0,
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
            "source": "ADEME Base IMPACTS \u00ae",
            "min": 4.85798e-08,
            "max": 4.85798e-08
        },
        "type": {
            "value": "pro",
            "status": "ARCHETYPE"
        },
        "units": {
            "value": 1,
            "status": "ARCHETYPE",
            "min": 1,
            "max": 1
        }
    }
}
```

</details>

This query returns :

* The impacts for both gwp and adp criteria since ```criteria=gwp&criteria=adp```
* The API will use an average electrical consumption of 70 Watt/hours 30% of the time (since ```use_time_ratio=0.3```) for one year (since duration is set at 8760 hours). 
* Usage impacts will be assessed for the French electrical mix impacts since ```usage_location='FRA'```
* Embedded impacts will be allocated on one year (since duration is set at 8760 hours).


For further information see : [The explanation page on terminal and peripherals](../Explanations/devices/terminals_&_peripherals.md)