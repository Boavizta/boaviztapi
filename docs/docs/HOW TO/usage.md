# Usage

Each device can have a ```usage``` object.

``` json
"usage": {
    "max_power": 510,
    "year_use_time": 3,
    "usage_location": "FRA",
    "workload": {
      "100": {
        "time": 0.15,
        "power": 1.0
      },
      "50": {
        "time": 0.55,
        "power": 0.7235
      },
      "10": {
        "time": 0.2,
        "power": 0.5118
      },
      "idle": {
        "time": 0.1,
        "power": 0.3941
      }
    }
  }
```
*Example for a dellR740 server*

## Duration attributes

The API handles three different time units :

| time unit | Usage parameter      |
|------     |-----------------     |
| HOURS     | ```hours_use_time``` |
| DAYS      | ```days_use_time```  |
| YEARS     | ```years_use_time``` |

If no duration is given, **the impact is measured for a year**.

*Note* : units are cumulative, if multiple units are used, they are summed.

### Example

```json
"usage":{
  "hours_use_time": 1,      
  "days_use_time": 1,
  "years_use_time":  1
}
```

will be converted in **8785** hours (```1+1*24+1*24*365```).

## Electrical impact factors

If you give your own electrical impact factor, the api will use it. 

### Example

```json
"usage":{
  "gwp_factor": 0.055
}
```
## Usage location

You can use the device location instead of giving an electrical impact factor.

```usage_location``` attribute describe the usage country. The country is represented as as trigram (usually the first three letter of the country).

By default, ```usage_location``` is set as ```EU27+1``` (Europe of the 27 + England)

### Example

```json
"usage":{
  "usage_location": "FRA"
}
```

## Electrical consumption

```hours_electrical_consumption``` is the medium electrical consumption in Watt per hour. 
If given, it will be used by the API.


## Workload and max power

If unknown, ```hours_electrical_consumption``` can be retrieved with a ```workload``` object. [See functional documentation](../FUNCTIONNAL/usage.md#retrieving-electrical-consumption)

```max_power``` correspond to the nominal power (specify by the constructor). 

Workload is an object segmented into one to many loads. 

A load is a quantity of resource usage. Each load has :

* A ```time``` : ratio of time when the device is running at this load. 
* A ```power```: power consumption at this load. **Express as a ratio of ```max_power```**

*note : the sum of the ```time``` attributes of all the loads must be 1*

### Incomplete workload

If you don't know the ```power``` per load of your device, you might need to use the ```power``` per workload of an archetype. In that case you should specify only the ```time``` per load.
Be sure to use a load segmentation supported by the archetype.

**Supported archetype loads : **

* 100%
* 50%
* 10%
* IDLE
* OFF

