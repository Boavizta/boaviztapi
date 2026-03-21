# Configuration

The API can be configured to use different defaults for locations and hardware specs, as well as different levels of precision.

The full list of configuration parameters and their defaults can be found in [`boaviztapi/utils/config.py`](https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi/utils/config.py).

## Overriding default values

Each variable can be overridden using an environment variable of the same name, prefixed with `BOAVIZTA_`.

For example, the `default_server` parameter can be overridden with the environment variable, `BOAVIZTA_DEFAULT_SERVER`.

## CORS

By default, all origins are allowed, but can be changed with the `BOAVIZTA_ALLOWED_ORIGINS` environment variable with the following format:

```
BOAVIZTA_ALLOWED_ORIGINS = '["url1", "url2", ...]'
```

For example: `BOAVIZTA_ALLOWED_ORIGINS='["https://datavizta.boavizta.org","https://boavizta.org"]'`.

## Special message

You can customize the home page with a special message by setting the environment variable `BOAVIZTA_SPECIAL_MESSAGE` in HTML format.

For example: `BOAVIZTA_SPECIAL_MESSAGE="<p>my welcome message in HTML format</p>"`

## Default location

The default location will be used if the user does not specify a `usage_location` in the request. The parameter is used to complete the impact of electricity.

```
default_location: "EEE"
```

This can be overridden with the `BOAVIZTA_DEFAULT_LOCATION` environment variable.

## Default archetype

The default archetype will be used if the user does not specify an `archetype` in the request. Note that it must match an existing archetype ID in the archetype files.

```
default_cpu: "DEFAULT"
default_server: "compute_medium"
```

These can be overridden with the `BOAVIZTA_DEFAULT_CPU` and `BOAVIZTA_DEFAULT_SERVER` environment variables.

## Default criteria

The default criteria will be used if the user does not specify the `criteria` in the request.

```
default_criteria: ["gwp", "adp", "pe"]
```

This can be overridden with the `BOAVIZTA_DEFAULT_CRITERIA` environment variable.

## Minimal significant figures

The minimal number of significant figures will be employed if classical rounding yields a result containing more significant figures than the minimal allowed.

```
min_sig_fig: 1
```

*If set to 1, the results will be rounded at least to 1 significant figures.*

This can be overridden with the `BOAVIZTA_MIN_SIG_FIG` environment variable.

## Maximal significant figures

The maximum number of significant figures will be employed if classical rounding yields a result containing more significant figures than the maximum allowed.

```
max_sig_fig: 5
```

*If set to 5, the results will be rounded to a maximum of 5 significant figures.*

This can be overridden with the `BOAVIZTA_MAX_SIG_FIG` environment variable.

## Uncertainty percentage

Uncertainty percentage is used to adapt the intensity of the rounding. The lower the uncertainty percentage, the lower aggressive the rounding.

```
uncertainty: 10
```

*If set to 10, the rounding aggressiveness will be set to 10%.*

This can be overridden with the `BOAVIZTA_UNCERTAINTY` environment variable.

## CPU name fuzzymatch threshold

The CPU name fuzzymatch threshold will determine the minimum similarity between the CPU name in the request and the CPU name in the database. If the similarity is lower than the threshold, the API will not use the match.

```
cpu_name_fuzzymatch_threshold: 62
```

This can be overridden with the `BOAVIZTA_CPU_NAME_FUZZYMATCH_THRESHOLD` environment variable.

## Electricity Maps integration

The Electricity Maps integration can be activated by setting the `electricity_maps_api_key` parameter. This can be overridden with the `BOAVIZTA_ELECTRICITY_MAPS_API_KEY` environment variable.
