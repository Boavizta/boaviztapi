# Configuration

Most configuration is managed in the YAML file `boaviztapi/data/config.yaml`, while CORS and the Special Message are managed via environment variables.

## CORS

By default, all origins are allowed, but can be changed with the `ALLOWED_ORIGINS` environment variable with the following format: `ALLOWED_ORIGINS = '["url1", "url2", ...]'`.

For example, `ALLOWED_ORIGINS='["https://datavizta.boavizta.org","https://boavizta.org"]'`

## Special message

You can customize the home page with a special message by setting the env value `SPECIAL_MESSAGE` in HTML format.

Example : `SPECIAL_MESSAGE="<p>my welcome message in HTML format</p>"`

## Default location

The default location will be used if the user does not specify a `usage_location` in the request.
The parameter is used to complete the impact of electricity.

```
default_location: "EEE"
```

## Default archetype

The default archetype will be used if the user does not specify an `archetype` in the request.
Note that it must match an existing archetype ID in the archetype files.

```
default_cpu: "DEFAULT"
default_server: "compute_medium"
```

## Default criteria

The default criteria will be used if the user does not specify the `criteria` in the request.

```
default_criteria: ["gwp", "adp", "pe"]
```

## Minimal significant figures

The minimal number of significant figures will be employed if classical rounding yields a result containing more significant figures than the minimal allowed.

```
min_sig_fig: 1
```

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

*If set to 10, the rounding aggressiveness will be set to 10%.*

## CPU name fuzzymatch threshold

The CPU name fuzzymatch threshold will determine the minimum similarity between the CPU name in the request and the CPU name in the database. If the similarity is lower than the threshold, the API will not use the match.

```
cpu_name_fuzzymatch_threshold: 62
```
