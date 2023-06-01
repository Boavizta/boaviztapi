# Archetypes

An archetype is a pre-recorded asset (device or component).

Archetype can be used :

* To create profiles for device with pre-recorded configuration components and usage. *For example : a medium storage server*

* To pre-record real devices *For example : dellr740*

Each type of device or component have a default archetype which can be changed in the configuration file.

## Using archetype in GET routes

You can specify an archetype in the route parameters when you send a device or a component to the API via a GET method. In this case, the API will compute the impacts of this specific archetype.

### Example

```GET /v1/server?archetype=dellR740``` : will return the impact of the pre-recorded dellR740.

## Using archetype in POST routes

You can specify an archetype in the route parameters when you send a device or a component to the API via a POST method. In this case the missing values will be completed with the values taken from the archetype.

### Example

```POST /v1/server?archetype=compute_medium```

```json
{
    "configuration": {
        ...
    },
    "usage": {
        ...
    }
}
```

In this case the missing values will be completed with the values taken from a *compute_medium* server.

## GET the list of available archetypes

You can get the list of available archetypes by using the GET method on the route ```{assets}/archetypes```.

## GET the configuration of an archetype

You can get the configuration of an archetype by using the GET method on the route ```{assets}/archetype_config?archetype={archetype}```.