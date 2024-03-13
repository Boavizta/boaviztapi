# Auto-complete information required for computation

Any calculation using the API is made easier thanks to the **data auto-complete strategy**. Any valid input should return an impacts evaluation, even though it is lacking some detailed information about the asset. Given the user inputs, the API finds the best strategy to fill any missing attributes for the computation. 

the API implements several approaches to complete the missing information:

* ```COMPELETE``` : The API infer the value based on the user inputs (e.g. `manufacturer` and `family` for a CPU ```name```).  
* ```DEFAULT``` : The API use a default value for those missing attributes (e.g. europe for the default ```usage_location```). The default values can be set in the [configuration file](../config.md).
* ```ARCETYPE``` : The API can use a value taken from an [archetype](archetypes.md).
* ```CHANGED```: The API can change the value of an attribute to make the computation possible. This happens when you provide a value that is close to the value of an attribute but not exactly the same. For example, if you provide a ```family``` that is not in the database but is close to a family in the database, the API will change the ```family``` to the closest name in the database.

The documentation about how attributes are auto-completed is given on each asset's documentation page. 

All attributes that are auto-completed by the API can be found in the [verbose](verbose.md) information. Attributes with a `status` of `ARCHETYPE`, `DEFAULT` or  `COMPLETED` are respectively using an archetype value, a default value or using an inferred value given user inputs.

## Example on a CPU

To provide a response to the following query that is lacking key information to compute the embedded impacts, some attributes will be auto-completed by the API.

```shell
curl -X 'POST' \
  'https://api.boavizta.org/v1/component/cpu?verbose=false&allocation=TOTAL' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "manufacturer": "Intel",
  "family": "Haswell"
}'
```

The response verbose will look like the following. 

```json
{
  ...
    "core_units": {
      "value": 24,
      "status": "ARCHETYPE",
      "min": 1,
      "max": 64
    },
    "die_size_per_core": {
      "value": 0.35,
      "status": "COMPLETED",
      "unit": "mm2",
      "source": "https://en.wikichip.org/wiki/intel/microarchitectures/haswell_(client)#Octadeca-core",
      "min": 0.35,
      "max": 0.44
    },
    "family": {
      "value": "haswell",
      "status": "CHANGED"
    },
    "time_workload": {
      "value": 50,
      "status": "ARCHETYPE",
      "unit": "%",
      "min": 0,
      "max": 100
    },
    "usage_location": {
      "value": "EEE",
      "status": "DEFAULT",
      "unit": "CodSP3 - NCS Country Codes - NATO"
    }
  ...
}
```

* usage_location is set by ```DEFAULT```.
* family is ```CHANGED``` since ```Haswell``` should be lowercase.
* die_size_per_core is set by ```COMPLETED``` since the value is inferred from the user inputs.
* time_workload is set by ```ARCHETYPE``` since the value is taken from the archetype.