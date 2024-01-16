## v1.2.0

## What's Changed

Adding new cloud instances is now easier. Simply define the resources they reserve and identify the server archetype on which the instance will be hosted. Refer to the [contribution](contributing) documentation for more information. 

### Internal changes

* Externalizing impacts computation outside the asset's model by creating a service for this purpose (boaviztapi/service/impacts_computation.py)
* Updating cloud instance model and impacts computation in line with : https://github.com/Boavizta/boaviztapi/issues/252#issuecomment-1845967609
* Improve impact model (boaviztapi/model/impact.py). All the assets keep the impacts as an attribute once they have been calculated. Performance is significantly improved in the event of a verbose call.

### bug fixes

* Power consumption was modelled for one component unit. Consumption was only multiplied by the number of components when calculating impacts at device level. The consumption of the component now reflects the consumption of all the units. 
* https://github.com/Boavizta/boaviztapi/issues/256
* https://github.com/Boavizta/boaviztapi/issues/257

### Contributors

@da-ekchajzer
@samuelrince
@JacobValdemar

## v1.1.0

## What's Changed

* Add independent Dockerfile by @JacobValdemar in https://github.com/Boavizta/boaviztapi/pull/239
* Add missing aws instances by @JacobValdemar and @github-benjamin-davy in https://github.com/Boavizta/boaviztapi/pull/237

**Full Changelog**: https://github.com/Boavizta/boaviztapi/compare/v1.0.1...v1.1.0

### Contributors

@JacobValdemar
@github-benjamin-davy
@da-ekchajzer

## v1.0.0

### New features

* Add new end-user devices from Base Empreinte 
* Add PEF impacts criteria
* Add IoT device impacts
* Add min/max values depending on user input completeness
* Add warnings
* Improvement of the completion process from CPU name
* Adding around 2000 CPUs for completion
* Adding utils routers (list available data for string fields, archetypes routers, etc.)
* Users can now choose the impact factors to compute
* Users can now add a special message to the home page of the API
* Refactor and normalize routes names
* CPU die is now express in mm2 instead of cm2
* Refactor the allocation process based on duration

### Internal changes

* Facilitating the completion process
* Facilitating the process of adding new devices
* Facilitating the archetype process
* Externalize the impact factors in a separate file
* Create a config file
* CPU die completion now use cpu spec file
* CPU uses die_size instead of die_size_per_core

### Breaking changes

#### Cloud routers

##### Before

* We add one rout per cloud provider (e.g. ```/v1/cloud/aws```)

##### Now

* We have only one route for all cloud providers (e.g. ```/v1/cloud/instance```)
* Each route has a parameter called ```provider``` (in the url for GET requests, in the body for POST requests).

#### Duration & allocation

##### Before

* Duration was a field in the usage object called ```hours_use_time```.

```
{
  "usage": {
    "hours_use_time": 2,
  }
}
```

* Allocation was a route parameter.

##### Now

* Duration is now a route parameter. Allocation is no longer used
* If not provided, we use the lifetime of the device as duration.
* We compute usage impacts over the ```duration``` and allocate embedded impacts on the ```duration``` over the lifetime of the device.
* We introduce the notion of ```use_time_ratio``` which is the proportion of time the device is used during the given duration. When a device is always used, the usage ratio is 1. When a device is never used, the usage ratio is 0.

```
{
  "usage": {
    "use_time_ratio": 0.5,
  }
}
```

#### Impacts format

##### Before
```json
"gwp": {
      "manufacture": 1900,
      "use": 260,
      "unit": "kgCO2eq"
    },
```
or
```json
"manufacture_impacts": {
        "gwp": {
          "value": 23.8,
          "unit": "kgCO2eq"
        },
        "pe": {
          "value": 353,
          "unit": "MJ"
        },
        "adp": {
          "value": 0.02,
          "unit": "kgSbeq"
        }
      }
}
```
##### Now

* Impact formats are now unified.
* "manufacture" is now called "embedded"

```json 
"impacts": {
   "gwp": {
     "embedded": {
       "value": 6.68,
       "min": 6.68,
       "max": 6.68,
       "warnings": [
         "End of life is not included in the calculation"
       ]
     },
     "use": "not implemented",
     "unit": "kgCO2eq",
     "description": "Total climate change"
   },
```

#### Verbose format

##### Before

```json
"USAGE": {
  ...
  "usage_impacts": {
       ...
  }
  "avg_power": {
    "value": 94.62364134445255,
    "unit": "W",
    "status": "COMPLETED",
    "source": null
  },
...
}
```

##### Now

* For each component, all attributes are now at the same level in the dictionary. 
* Usage impacts are now in the "impacts" dictionary
* Usage attributes are now at the same level as the other attributes
* Attributes may have a "min", a "max" and a "warnings" field.

```json
  "CPU-1": {
      "impacts": {
        "gwp": {
          "embedded": {
            "value": 64.7,
            "significant_figures": 3,
            "min": 24.6,
            "max": 149,
            "warnings": [
              "End of life is not included in the calculation"
            ]
          },
          "use": {
            "value": 160,
            "significant_figures": 2,
            "min": 160,
            "max": 160
          },
          "unit": "kgCO2eq",
          "description": "Total climate change"
        }
      },
      "die_size_per_core": {
        "value": 0.47078947368421054,
        "status": "COMPLETED",
        "unit": "mm2",
        "source": "Average for Skylake",
        "min": 0.07,
        "max": 1.02
      }
      ... 
}
```

### Contributors

@airloren
@csauge
@da-ekchajzer
@samuelrince
@dorev
@demeringo
@PierreRust

### Known future requirements

* Mobile and fix network impacts
* Generalize the AWS process to other cloud providers
* GPU impacts
* Add multiple impact factors for depending on the engraving process size
* Screen impacts from characteristics
* Take into account the uncertainty of the impact factors
* Adding a system layer

## v0.2.2

### What's Changed

* Change CPU manufacturing impact formula by @samuelrince in https://github.com/Boavizta/boaviztapi/pull/142
* reduce docker image size using distroless by @AirLoren in https://github.com/Boavizta/boaviztapi/pull/141
* Modify cloud route to allow multiple cloud providers by @AirLoren in https://github.com/Boavizta/boaviztapi/pull/139

### New Contributors
* @AirLoren made his first contribution in https://github.com/Boavizta/boaviztapi/pull/141

**Full Changelog**: https://github.com/Boavizta/boaviztapi/compare/v0.2.1...v0.2.2

## v0.2

### Goal

v0.2 contains significant changes to the code to facilitate the addition of new features. The main additional functionality is the ability to model the power consumption of certain components, servers and cloud instances from their configuration.

### Improvements

* Implementing linear allocation for manufacturing impacts
* Implementing fuzzy matching for string fields 
* Model electrical consumption from technical characteristics and usage context for CPU, RAM, Server and Cloud instance 
* Complete CPU info from CPU name
* Adding source, units and status for each attributes in verbose mode
* Adding utils routers (list available data for string fields)
* Storing all data in CSV format
* Ease the deployment of API as a serverless application
* Documentation improvements
* Improving CORS settings
* Adding new AWS EC2 instances

### Known future requirements

* Mobile and fix network impacts
* Screen impacts
* Workplace impacts
* IoT impacts
* Generalize AWS process to other cloud providers
* GPU impacts
* Add multiple impact factors for semiconductors
* Add multiple impacts factors for impacts related to electricity


## v0.1.2

### Bug

### missing W to kW conversion

```hour_electical_consumption``` should be given in Watt.
When avg_power was directly given (in watt) the value was used in Wh. The electrical impacts factor requires kWh.

### Correction

Adding conversion from W to kW ( / 1000) when ```hour_electical_consumption``` is used with an electrical impact factor.

### PR

https://github.com/Boavizta/boaviztapi/pull/93


## V0.1.1

### Goal

The V0.1.1 adds new CPU data and electrical impact factors.

### Improvements

* Adding new CPUs
* Implement PE and ADP impact for use phase
* Improvement of gwp impacts factor quality

### Known future requirements

* Mobile and fix network impacts
* Screen impacts
* Workplace impacts
* IoT impacts
* Generalize AWS process to other cloud providers

## v0.1

### Goal

The V0.1.0 introduces the notions of archetypes, verbose and units. An implementation of AWS instances impacts have been implemented. Impact of usage have also been developed.

### Functionalities

* Retrieve the impacts of AWS instances
* Retrieve the impacts of server archtypes
* Retrieve usage imapcts (GWP only) of usage
* Verbose option
* Bug fix
* Work on documentation

### Known future requirements

* Mobile and fix network impacts
* Screen impacts
* Workplace impacts
* IoT impacts
* Generalize AWS process to other cloud providers


## V0

### Goal

The V0 is the MVP of Boavizta tools api.
It aims at giving access to the server bottom-up methodology measuring the scope 3 of servers explain in this article :

https://boavizta.cmakers.io/blog/numerique-et-environnement-comment-evaluer-l-empreinte-de-la-fabrication-d-un-serveur-au-dela-des-emissions-de-gaz-a-effet-de-se?token=2112aecb183b1b5d27e137abc61e0f0d39fabf99

### Project setup

* Setup python project (fastAPI)
* Setup project test (pytest)
* Setup project documentation (mkdocs)
* Setup CI/CD (gitworkflow - git repository)
* Creation of the theoretical architecture

### Functionalities

* Retrieve the manufacture impact of components from its characteristics
* Retrieve the manufacture impact of servers from its characteristics with the bottom-up methodology
* Complete the server or component characteristic if incomplete data are sent by the user

### Known future requirements

* Bug fix
* Returns a verbose object (hypothesis, modify datas, calculation steps)
* Integrate Boavizta database
* Implement new devices
* Support use case implementations
* Implement scope 1 & 2