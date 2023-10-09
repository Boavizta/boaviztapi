🎯 Retrieving the impacts of digital elements.

This is a quick demo, to see full documentation [click here](https://doc.api.boavizta.org)

## Features

Bellow a list of all available features.

### 👄 Verbose

Verbose is an HTTP parameter. If set at true :

* Shows the impacts of each component
* Shows the value used for each attribute

*"attribute": {"value": "value", "unit": "unit", "status": "Status", "source": "Source", "min":"min", "max":"max", "significant_figures":"significant_figures"}*

### 🔨 Embedded
 
* Embedded impacts are the impacts occurring during raw material extraction, manufacture, distribution and end of life
* When end of life is not taken into account, we specified it in the ```warnings```

### 🔌  Usage

Usage impacts are assessed by multiplying :

 * a **duration**

 * an **impact factor** 

 * an **electrical consumption** 

#### ⏲ Duration

Usage impacts can be given as a router parameter, in hours.

If no duration is given, **the impact is assess for the all life duration of the asset**.


#### ✖️ Impact factors

* Impact factors can be given : *"usage":{"elec_factors":{[criteria]: 0.38}}*
* Impact factors can be retrieved from : *"usage":{"usage_location": "FRA"}*. 

* See the list of locations : [/v1/utils/country_code](/v1/utils/country_code)*

#### ⚡ Electrical consumption

##### ⏺️ Given
* Electrical consumption can be given for one hour (average) *"usage":{"avg_power": 1}*.

##### 📈 Modeled
* Electrical consumption can be retrieved from consumption profile using *usage:{time_workload: 50}*.

##### 📋 Archetype

* In some cases, default electrical consumption can be taken from the archetype

### 🔃 Auto-complete & 📋 Archetype

The API will complete the missing attributes in a request with a completion function or with values
taken from the ```archetype``` specified in the route parameter.

### ⏬ Allocation

* Usage impacts are assessed on the duration given in route parameter
* Embedded impacts are allocated linearly on the duration given in parameter
```embedded_impact = impact * (duration/life_duration)```

If no duration is given, the life_duration (```hours_life_time``) of the asset is used.