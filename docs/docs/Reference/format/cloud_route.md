# Cloud route

!!!warning
    Before v1.2, the impacts in the verbose dictionary qualified the impacts of the component of the whole server hosting the instance. Since v1.2, the impacts in the verbose dictionary are the impacts of the part of the component used by the instance itself.

!!!warning
    Archetype are renamed ```instance_type``` and are specific to a ```provider```. In GET routes, you can specify the ```provider``` and the ```instance_type``` in the route parameters. In POST routes, you can specify the ```provider``` and the ```instance_type``` in the object.

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

### Examples

*time_workload is given as a dictionary*

```json
{
  "provider": "aws",
  "instance_type": "r6g.medium",
  "usage":{
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
    "usage_location": "FRA",
    "time_workload": 34
  }
}
```

