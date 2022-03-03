# Cloud route

Only AWS in implemented for now.

##```/v1/cloud/aws```

A cloud instance input is composed of a single objects : ```usage``` and a ```instance_type``` query attribute.

```json
{
"usage":{}
}
```

```model``` and ```configuration``` are retrieve from the pre-register ```instance_type```.

### Minimal server input

You can send an empty cloud instance :

```json
{}
```

or 

```json
{
"usage":{}
}
```

In this case, default value from ```instance_type``` are used


### Usage

```usage``` for cloud instances are particular. Most of the needed attributes are pre-registered in the ```instance_type```.
You should only set :

* ```usage_location``` with the location of the instance - *By default, ```usage_location``` is set as ```EU27+1``` (Europe of the 27 + England)*



* Duration - *By default, 1 year is used.*
    - ```hours_use_time```
    - ```days_use_time```
    - ```years_use_time```

  
* ```time``` per load for - *By default, we will consider the instance running at 50% all the duration*
    - 10%
    - 50%
    - 100%
    - idle

  
### Example

```json
{
"usage":{
    "usage_location": "BEL",
    "workload":{
        "10":{
          "time": 0.1
        },
        "50":{
          "time": 0.2
        },
        "100":{
          "time": 0.1
        },
        "idle":{
          "time": 0.5
        }
    }
  }
}
```