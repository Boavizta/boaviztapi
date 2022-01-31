### Configuration

Each device have a ```configuration``` object. 
A configuration contains zero to several components.

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
*Example for the dellR740 server*

### Incomplete configuration

If the minimal components of a device are not sent they are replaced by default components or components from the archetype if specified.

