# Archetypes

**Work in progress**

An archetype is a pre-recorded device.

Archetype can be used :

* To create profiles for device with pre-recorded configuration components and usage. *For example : a high performance server.*

* To pre-record real devices *For example : dellr740*


## Using archetype in /model routes

You can retrieve the impacts of a specific archetype by specifying its name in the /model routes of devices. 

### Example

```/v1/server/model?archetype=dellR740``` : will return the impact of the pre-recorded dellR740.

## Using archetype in model object

You can specify an archetype in the model of a device when you send a device to the api.
When doing so, missing data are retrieved from the archetype instead of default data.

### Example

```json
{
  "model":
  {
    ...
    "archetype": "dellR740"
  },
  "config": {
    ...
  },
    "usage": {
        ...
 }
}
```

All the missing data will be set with the corresponding data of the dellR740.