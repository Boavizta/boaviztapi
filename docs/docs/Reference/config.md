
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
default_cpu: "DEFAULT"
default_server: "compute_medium"
```

## Default_criteria

The default criteria will be used if the user does not specify the ```criteria``` in the request.

```
default_criteria: ["gwp", "adp", "pe"]
```

## Minimal significant figures

The minimal significant figures will be used to round the results of the API.

```
min_significant_figures: 5
```

*If set to 5, the results will be rounded to 5 significant figures.*

## CPU name fuzzymatch threshold

The CPU name fuzzymatch threshold will determine the minimum similarity between the CPU name in the request and the CPU name in the database. If the similarity is lower than the threshold, the API will not use the match.

```
cpu_name_fuzzymatch_threshold: 62
```