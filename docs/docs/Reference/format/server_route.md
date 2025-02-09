# DeviceServer route

## POST ```/v1/server/```

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

In this case, only default values are used.

### Configuration

#### Minimal configuration

If any of those following components aren't sent, a default component will be added to the configuration.

* [CPU](../../Explanations/components/cpu.md)
* [RAM](../../Explanations/components/ram.md)
* [SSD](../../Explanations/components/ssd.md)
* [HDD](../../Explanations/components/hdd.md)
* [power supplies](../../Explanations/components/power_supply.md)
* [case](../../Explanations/components/case.md)


#### Complete input

The Dell R740 is a good example of a well-defined server configuration input. 
Specific needed data are sent to apply the bottom-up methodology.

``` json
{
    "configuration":
    {
        "cpu":
        {
            "units": 2,
            "core_units": 24,
            "die_size_per_core": 245
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

Some required attributes are unknown, but some component attributes are given so specific die size can be retrieved by the API

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

## GET ```/v1/server```

See [archetypes documentation](../../Explanations/archetypes.md)
