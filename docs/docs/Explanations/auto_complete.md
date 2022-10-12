# Auto-complete information required for computation

Any calculation using the API is made easier thanks to the **data auto-complete strategy**. Any valid input should return an impact evaluation, even though it is lacking some detailed information about the component, device or cloud instance. Given the user inputs, the API finds the best strategy to fill any missing attributes for the computation. 

Depending on the type of calculation and component, device or cloud instance, the API will **either infer or use default values** for those missing attributes. The documentation about how attributes are auto-completed is given on each component, device or cloud instance documentation page. 

All attributes that are auto-completed by the API can be found in the [verbose](verbose.md) information. Attributes with a `status` of `DEFAULT` or `COMPLETED` is respectively using a default value or using an inferred value given user inputs.

## Example on a CPU

To provide a response to following query that is lacking key information to compute the manufacturing impact, some attributes will be auto-completed by the API.

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

The response verbose will look like the following. The `core_units` and `die_size_per_core` attributes are mandatory to compute manufacturing impact, thus they are `COMPLETED` by the API using user inputs `manufacturer` and `family`. Note that you can check the source of the value used.

```json
{
    ...
    "verbose": {
        ...
        "core_units": {
            "value": 18,
            "unit": "none",
            "status": "COMPLETED",
            "source": "https://en.wikichip.org/wiki/intel/microarchitectures/haswell_(client)"
        },
        "die_size_per_core": {
            "value": 0.346,
            "unit": "mm2",
            "status": "COMPLETED",
            "source": "https://en.wikichip.org/wiki/intel/microarchitectures/haswell_(client)"
        }
        ...
    }
}
```
