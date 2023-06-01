
The config file located at data/config.json is used to set default values for the following parameters.

## Default location

The default location will be used if the user does not specify a ```usage_location``` in the request. 
The parameter is used to complete the impact of electricity.

```
default_location: "EEE"
```

## Default archetype

The default archetype will be used if the user does not specify an ```archetype``` in the request.
Note that it must match an existing archetype ID in the archetype files.

```
..
default_cpu: "DEFAULT"
default_server: "compute_medium"
...
```

## Default_criteria

The default criteria will be used if the user does not specify the ```criteria``` in the request.

```
default_criteria: ["gwp", "adp", "pe"]
```

## Default duration

The default duration for the assessment will be used
if the user does not specify the ```duration``` in the request as a query parameter.

```
default_duration:
```

*If no value is specified (like in the example above), the assessment will be performed for the full lifetime of the asset.*