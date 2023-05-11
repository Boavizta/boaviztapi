# Cloud route
!!!warning 
    Only AWS is implemented for now.

## GET ```/v1/cloud/```

The GET router will return the default impacts of a cloud instance. The query is composed of minimum two query parameters : a ```provider``` and an ```instance_type```.

```/v1/cloud/?provider=aws&instance_type=r6g.medium```

```usage``` will be set with default values, ```model``` and ```configuration``` are retrieve from the pre-register ```instance_type```.


## ``` POST /v1/cloud/```

The POST router lets you set the usage variables. You need to set a ```provider``` and an ```instance_type```. ```usage``` is optional.

```json
{
  "provider": "aws",
  "instance_type": "r6g.medium",
  "usage": {}
}
```

```model``` and ```configuration``` are retrieve from the pre-register ```instance_type```.

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
  "provider": "aws",
  "instance_type": "r6g.medium",
  "usage":{
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
}
```

*time_workload is given as a percentage*

```json
{
  "provider": "aws",
  "instance_type": "r6g.medium",
  "usage": {
    "hours_use_time": 2,
    "usage_location": "FRA",
    "time_workload": 34
  }
}
```

