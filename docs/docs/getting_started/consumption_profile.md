# Getting started (5 min)

This page presents basic queries that can be used to generate and use consumption profiles.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/consumption_profile/cpu' | jq`)_


## Generate a cpu consumption profile from TDP

In this query we generate consumption profile parameters (a,b,c,d) from a TDP and a model_range

```cpu_consumption_profile(workload) = a * ln(b*(workload + c)) + d```

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/consumption_profile/cpu' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "cpu": {
    "name": "intel xeon gold 6134",
    "tdp": 130
    }
  }'
```

Result :

The API will select the average xeon gold consumption profile and adapt it with a TDP of 130 Watt.

```json
{
  "a": 35.5688,
  "b": 0.2438,
  "c": 9.6694,
  "d": -0.6087
}
```

## Generate a cpu consumption profile from workloads

In this query we generate consumption profile parameters (a,b,c,d) from a workload datapoints and a model_range

```cpu_consumption_profile(workload) = a * ln(b*(workload + c)) + d```

```bash
curl -X 'POST' \
  '{{ endpoint }}/v1/consumption_profile/cpu' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "cpu": {
    "name": "intel xeon gold 6134"
  },
  "workload": [
    {
      "load_percentage": 0,
      "power_watt": 50
    },
    {
      "load_percentage": 10,
      "power_watt": 100
    },
    {
      "load_percentage": 50,
      "power_watt": 180
    },
    {
      "load_percentage": 100,
      "power_watt": 245
    }
  ]
}'
```

Result :

The API will select the average xeon gold consumption profile and adapt it to match the given datapoints

```json
{
  "a": 88.92199999999995,
  "b": 0.13034943934208817,
  "c": 13.521235682053703,
  "d": -0.6456240344253034
}
```

For further information see : [The explanation page on consumption profiles](../Explanations/consumption_profile.md)