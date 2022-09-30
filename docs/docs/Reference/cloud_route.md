# Cloud route

Only AWS in implemented for now.

## ```/v1/cloud/aws```

A cloud instance input is composed of a single objects : ```usage``` and a ```instance_type``` query attribute.

```json
{
"usage":{}
}
```

```model``` and ```configuration``` are retrieve from the pre-register ```instance_type```.

### Minimal cloud input

You can send an empty cloud instance :

```json
{}
```

In this case, default value from ```instance_type``` are used

### Usage

```usage``` for cloud instances are particular. Most of the needed attributes are pre-registered in the ```instance_type```.
You should set :

* ```usage_location```
* ```time_workload```
* Duration :
    - ```hours_use_time```
    - ```days_use_time```
    - ```years_use_time```

### Examples

*time_workload is given as a dictionary*

```json
{
  "hours_use_time": 2,
  "usage_location": "FRA",
  "time_workload": [
    {
      "time_percentage": 50,
      "load_percentage": 0
    },
    {
      "time_percentage": 25,
      "load_percentage": 60
    },
    {
      "time_percentage": 25,
      "load_percentage": 100
    }
  ]
}
```

*time_workload is given as a percentage*

```json
{
  "hours_use_time": 2,
  "usage_location": "FRA",
  "time_workload": 34
}
```

