# Usage

Usage impacts can be measured at device or component level from usage configuration.

## General

*```hours_electrical_consumption``` is given Watt. The usage location is given as a trigram (see available country code). The duration is given in day, hours and years (units are cumulative)*

```json
{
 "usage": {
   "days_use_time": 1,
   "hours_use_time": 1,
   "years_use_time": 1,
   "usage_location": "FRA",
   "hours_electrical_consumption": 120
 }
}
```

## Modeled

When ```hours_electrical_consumption``` is unknown, it can be retrieved from ```time_workload```

### ```/v1/server/```

*```time_workload``` is given as a percentage at server level. The electrical consumption will be model for a load of 50% from RAM and CPU characteristics. The consumption of the other components are set relatively to the consumption of RAM and CPU with the ```other_consumption_ratio```*

```json
{
  "usage": {
    "time_workload": 50,
    "other_consumption_ratio": 0.33
  },
  "configuration": {
    "cpu": {
       "name": "Intel Xeon Gold 6138f"
    },
    "ram": {
       "capacity": 32
    }
  }
}
```

*```time_workload``` is given as a dictionary at server level*

```json
{
  "usage": {
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
  },
  "configuration": {
    "cpu": {
      "name": "Intel Xeon Gold 6138f"
    },
    "ram": {
      "capacity": 32
    }
  }
}
```

*```time_workload``` is given as a percentage at RAM and CPU level. The electrical consumption will be model for a load of 50% for CPU and 30% for the RAM*

```json
{
  "usage": {
    "other_consumption_ratio": 0.33
  },
  "configuration": {
    "cpu": {
       "name": "Intel Xeon Gold 6138f",
       "usage":{
            "time_workload": 50
        }
    },
    "ram": {
       "capacity": 32,
       "usage":{
            "time_workload": 30
        }
    }
  }
}
```

### ```/v1/component/ram```

*```time_workload``` is given in percentage at RAM level. The electrical consumption will be model for 32GB of RAM at 50% of load*

```json
{
 "capacity": 32,
 "usage": {
   "days_use_time": 1,
   "usage_location": "FRA",
   "time_workload": 50
 }
}
```

### ```/v1/component/cpu```

*```time_workload``` is given in percentage at CPU level. The electrical consumption will be model for a CPU with a TDP of 120 Watt at 50% of load*

```json
{
 "tdp": "120",
 "usage": {
   "days_use_time": 1,
   "usage_location": "FRA",
   "time_workload": 50,
 }
}
```

*```time_workload``` is given in percentage at CPU level. The electrical consumption will be model for a Xeon Gold CPU at 50% of load*

```json
{
 "name": "Intel Xeon Gold 6138f",
 "usage": {
   "days_use_time": 1,
   "usage_location": "FRA",
   "time_workload": 50,
 }
}
```

*```time_workload``` is given in percentage at CPU level. The electrical consumption will be model for a Xeon Gold CPU with a TDP of 220 Watt at 50% of load*

```json
{
 "name": "Intel Xeon Gold 6138f", 
 "tdp": 220,
 "usage": {
   "days_use_time": 1,
   "usage_location": "FRA",
   "time_workload": 50,
 }
}
```