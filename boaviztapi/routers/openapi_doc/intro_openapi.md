🎯 Retrieving the impacts of digital elements
This is a quick demo, to see full documentation [click here](https://doc.api.boavizta.org)

## Features

Bellow a list of all available features. Implemented features are specified for each route.

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
*Electrical consumption can be given for one hour (average) *usage:{hours_electrical_consumption: 1}*. See

##### 📈 Modeled
* Electrical consumption can be retrieved from consumption profile using *usage:{time_workload: 50}*. See : 

#### 🔃 Auto-complete

The API will complete the missing attributes in a request. Components have different completion strategies see :
Devices have minimal required components. If not given in the request a component with default characteristics are used. see :

#### 📋 Archetype

If an archetype is given, the missing attributes will be complete with the archetypes attributes instead of default attributes