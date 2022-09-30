🎯 Retrieving the impacts of digital elements.

This is a quick demo, to see full documentation [click here](https://doc.api.boavizta.org)

## Features

Bellow a list of all available features. Implemented features are specified in each route.

### 👄 Verbose

Verbose is an HTTP parameter. If set at true :
* Shows the impacts of each component
* Shows the value used for each attributes

*"attribute": {"value": "value", "unit": "unit", "status": "Status", "source": "Source"}*

### 🔨 Manufacture
 
* Manufacture impacts of devices are the sum of the impacts of its components
* Manufacture impacts equations of components are given for each component

### 🔌  Usage

Usage impacts are measured by multiplying :

 * a **duration**

 * an **impact factor** 

 * an **electrical consumption** 

#### ⏲ Duration

Usage impacts are given for a specific time duration. Duration can be given in :

* HOURS : *usage:{hours_use_time: 1}*
* DAYS : *usage:{days_use_time: 1}*
* YEARS : *usage:{years_use_time: 1}* 

If no duration is given, **the impact is measured for a year**.
*Note* : units are cumulative

#### ✖️ Impact factors

* Impact factors can be given : *usage:{[criterion]_factors: 0.38}*
* Impact factors can be retrieved from : *usage:{usage_location: "FRA"}*. See the list of usage location :

#### ⚡ Electrical consumption

##### ⏺️ Given
*Electrical consumption can be given for one hour (average) *usage:{hours_electrical_consumption: 1}*.

##### 📈 Modeled
* Electrical consumption can be retrieved from consumption profile using *usage:{time_workload: 50}*. 

### 🔃 Auto-complete

The API will complete the missing attributes in a request. Components have different completion strategies.
Devices have minimal required components. If not given in the request a component with default characteristics are used.

### 📋 Archetype

If an archetype is given, the missing attributes will be complete with the archetypes attributes instead of default attributes

### ⏬ Allocation

Allocation is an HTTP parameter. 

* If set at TOTAL, the total manufacture impact is returned.
* If set at LINEAR the manufacture impact is allocated linearly hover a specific lifespan given or set by default : {"usage":{"years_life_time":1}}