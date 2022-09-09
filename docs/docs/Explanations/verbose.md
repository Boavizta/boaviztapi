# Verbose

In the interest of transparency of our methods and data, all data used by the API can be described in the response to a request if the option verbose is set as true 

## Impacts per components

For each component evaluated in a request the total impacts of a single component are returned.

```json
"impacts": {
  "gwp": {
      "manufacture": 24,
      "use": "not implemented",
      "unit": "kgCO2eq"
  },
  "pe": {
      "manufacture": 293,
      "use": "not implemented",
      "unit": "MJ"
  },
  "adp": {
      "manufacture": 0.0011,
      "use": "not implemented",
      "unit": "kgSbeq"
  }
}
```

## Units

The number of unit per component in a device is returned.

```json
"units": 2,
```

## Boattribute

For each attribute used in the evaluation process we return :

* Its **value**
* Its **unit**
* Its **status** :
  * **INPUT** : the value have been given by the user
  * **COMPLETED** : the value have set by the API according to user inputs 
  * **DEFAULT** : the default value have been set by the API
  * **CHANGED** : the value have given by the user have been changed by the API
  * **ARCHETYPE** : the default value have been set by the API from the archetype
* The source of data in case the data have been COMPLETED or CHANGED

```json
"gwp_factor": {
  "value": 0.38,
  "unit": "KgSbeq/kWh",
  "status": "COMPLETED",
  "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149 : \nAverage of 27 european countries"
}
```
