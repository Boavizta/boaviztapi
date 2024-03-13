# Archetypes

An archetype is a pre-recorded asset (device or component).

Archetype can be used :

* To create profiles for device with pre-recorded configuration components and usage. *For example : a medium storage server*

* To pre-record real devices *For example : dellr740*

Each type of asset have a default archetype which can be changed in the configuration file.

## Using archetype in GET routes

You can specify an archetype in the route parameters when you send an asset to the API via a GET method. In this case, the API will compute the impacts of this specific archetype.

### Example

```GET /v1/server?archetype=dellR740``` : will return the impact of the pre-recorded dellR740.

## Using archetype in POST routes

You can specify an archetype in the route parameters when you send a device or a component to the API via a POST method. In this case the missing values will be completed with the values taken from the archetype.

### Example

```POST /v1/server?archetype=platform_compute_medium```

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

In this case the missing values will be completed with the values taken from a *platform_compute_medium* server.

## GET the configuration of an archetype

You can get the configuration of an archetype by using the GET method on the route ```{assets}/archetype_config```.

!!!warning
    For cloud instances, archetype works a bit differently. They are renamed ```instance_type``` and are specific to a ```provider```. In GET routes, you can specify the ```provider``` and the ```instance_type``` in the route parameters. In POST routes, you can specify the ```provider``` and the ```instance_type``` in the object. 