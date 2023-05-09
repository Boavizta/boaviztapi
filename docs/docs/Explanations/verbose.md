# Verbose

In the interest of transparency of our methods, data and source, all data used by the API can be described in the response to a request if the option ```verbose``` is set as true 

## Impacts per components

For each component evaluated in a request, the embedded and usage impacts of the component are returned

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
      }
```

## Boattribute

For each attribute used in the evaluation process, we return :

* Its **value**
* Its **unit**
* Its **unit** when relevant
* Its **min** value
* Its **max** value
* Its **status** :
     * **INPUT**: the value has been given by the user
     * **COMPLETED**: the value has set by the API according to user inputs 
     * **DEFAULT**: the default value has been set by the API
     * **CHANGED**: the value has been given by the user and has been changed by the API
     * **ARCHETYPE**: the default value has been set by the API from the archetype
* The **source** of data in case the data has been COMPLETED or CHANGED and sometimes when the DEFAULT value comes from a secondary source.

```json
"gwp_factor": {
  "value": 0.38,
  "status": "DEFAULT",
  "unit": "kg CO2eq/kWh",
  "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries",
  "min": 0.023,
  "max": 0.9
}
```