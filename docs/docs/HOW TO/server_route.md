# Server route

##```/v1/server/```

A server input is composed of 3 different objects : ```model```, ```configuration```, ```usage```

``` json
{
"model":{},
"configuration":{},
"usage":{}
}
```

### Minimal server input

You can send an empty server :

``` json
{}
```

or 

``` json
{
"model":{},
"configuration":{},
"usage":{}
}
```

In this case, only default value are used.

### Configuration

#### Minimal configuration

If any of those following components aren't sent, a default component will be added to the configuration.

* 1 CPU
* 1 RAM
* 1 SSD - TO MODIFY

#### Complete input

The Dell R740 is a good example of a well-defined server configuration input. 
Specific needed data are sent (in particular the die size) to apply the bottom-up methodology.

``` json
{
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

#### Incomplete input

The die size in unknown but some component's attributes are given so specific die size can be retrieved by the API

``` json
{
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
            "units": 2
        }
    }
}
```

#### Usage

See [usage](usage.md)

##```/v1/server/model```

See [archetypes documentation](../FUNCTIONNAL/archetypes.md#using-archetype-in-model-routes)
