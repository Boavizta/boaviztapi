
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

The minimal number of significant figures will be employed if classical rounding yields a result containing more significant figures than the minimal allowed.

```
min_sig_fig: 1
```

<<<<<<< HEAD
*If set to 1, the results will be rounded at least to 1 significant figures.*


## Maximal significant figures

The maximum number of significant figures will be employed if classical rounding yields a result containing more significant figures than the maximum allowed.
```
max_sig_fig: 5
```

*If set to 5, the results will be rounded to a maximum of 5 significant figures.*

## Uncertainty percentage

Uncertainty percentage is used to adapt the intensity of the rounding. The lower the uncertainty percentage, the lower aggressive the rounding.

```
uncertainty: 10
```
=======
*If set to 5, the results will be rounded to 5 significant figures.*

## CPU name fuzzymatch threshold

The CPU name fuzzymatch threshold will determine the minimum similarity between the CPU name in the request and the CPU name in the database. If the similarity is lower than the threshold, the API will not use the match.

```
cpu_name_fuzzymatch_threshold: 62
>>>>>>> 0416dde5deaffdb14496936b91c5c66b64570f9d
```