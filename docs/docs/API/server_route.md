# Server bottom-up route

```/v1/server/bottom-up```

## Minimum server input

You can send an empty server :

``` json
{}
```

In this case, only default value are used.

## Recommended input

The Dell R740 is a good example of a well-defined server input. 
Specific needed data are sent (in particular the die size) to apply the bottom-up methodology.

``` json
{
    "model":
    {
        "manufacturer": "Dell",
        "name": "R740",
        "type": "rack",
        "year": 2020
    },
    "configuration":
    {
        "cpu":
        {
            "units": 2,
            "core_units": 24,
            "die_size_per_core": 0.245
        },
        "ram":
        [
            {
                "units": 12,
                "capacity": 32,
                "density": 1.79
            }
        ],
        "disk":
        [
            {
                "units": 1,
                "type": "ssd",
                "capacity": 400,
                "density": 50.6
            }
        ],
        "power_supply":
        {
            "units": 2,
            "unit_weight": 2.99
        }
    }
}
```
*Dell R740 object*


## Usual type of input

The die size in unknown but some component's characteristic are given so specific die size can be retrieved by the API

``` json
{
    "model":
    {
        "type": "rack",
        "year": 2020
    },
    "configuration":
    {
        "cpu":
        {
            "units": 2,
            "core_units": 24,
            "family": "Skylake"
        },
        "ram":
        [
            {
                "units": 12,
                "capacity": 32,
                "manufacturer": "Samsung"
            }
        ],
        "disk":
        [
            {
                "units": 1,
                "type": "ssd",
                "capacity": 400,
                "manufacturer": "Samsung"
            }
        ],
        "power_supply":
        {
            "units": 2,
        }
    }
}
```
