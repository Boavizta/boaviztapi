# Model

Each device can have a ```model``` object.

``` json
{
  "model": {
    "manufacturer": "Dell",
    "name": "R740",
    "type": "rack",
    "year": 2020,
    "archetype": "high"
  }
}
```
*Example for a dellR740 server*

## Metadata 

Metadata are descriptive attributes not used in the calculation or completion process.
This type of attribute are not used for now in the api but could be used to implement search process.

* ```manufacturer```
* ```name```
* ```year```

## Archetype

See [archetypes documentation](../FUNCTIONNAL/archetypes.md#using-archetype-in-model-object)


## Type

Used to classify a device.

* For server ```type``` can be set at ```rack``` or ```blade```, the case component is set in consequence. 
