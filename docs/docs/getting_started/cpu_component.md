# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of a CPU. The requests for the other components are similar.

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' 'https://api.boavizta.org/v1/cloud/aws/all_instances' | jq`)_

## Get the impacts from cpu name

In this query, we use the cpu name to evaluate its impact.

Query : 

```bash
curl -X 'GET' \
  'http://localhost:5000/v1/component/cpu?verbose=false' \
  -H 'accept: application/json' \
  -d '{"name": "Intel Core i3-5157u"}'
```

This query returns :

* The impacts of the CPU on the all life cycle

Result :

```json
{
  "gwp": {
    "manufacture": 21.7,
    "use": "not implemented",
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 325,
    "use": "not implemented",
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.02,
    "use": "not implemented",
    "unit": "kgSbeq"
  }
}
```

## Get the values used to measure the impacts of the cpu

This is the same query as before. However, you add the `verbose=true` flag to get the value of the attributes used for the calculation.

```bash
curl -X 'GET' \
  'http://localhost:5000/v1/component/cpu?verbose=true' \
  -H 'accept: application/json' \
  -d '{"name": "Intel Core i3-5157u"}'
```

This query returns :

* The impacts of the CPU on the all life cycle
* The CPU characteristics used to evaluate these impacts

Result :

You can see that the API have complete the needed value from the cpu name. We parse and fuzzymatch the cpu name with our dataset of cpu to identify model_range, manufacturer and family.
The die_size_per_core is completed from the cpu family.

```json
{
  "impacts": {
    "gwp": {
      "manufacture": 21.7,
      "use": "not implemented",
      "unit": "kgCO2eq"
    },
    "pe": {
      "manufacture": 325,
      "use": "not implemented",
      "unit": "MJ"
    },
    "adp": {
      "manufacture": 0.02,
      "use": "not implemented",
      "unit": "kgSbeq"
    }
  },
  "verbose": {
    "units": 1,
    "impacts": {
      "gwp": {
        "value": 21.7,
        "unit": "kgCO2eq"
      },
      "pe": {
        "value": 325,
        "unit": "MJ"
      },
      "adp": {
        "value": 0.02,
        "unit": "kgSbeq"
      }
    },
    "core_units": {
      "value": 24,
      "unit": "none",
      "status": "DEFAULT",
      "source": null
    },
    "die_size_per_core": {
      "value": 0.245,
      "unit": "mm2",
      "status": "DEFAULT",
      "source": null
    },
    "model_range": {
      "value": "core i3",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    },
    "manufacturer": {
      "value": "intel",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    },
    "family": {
      "value": "broadwell",
      "unit": "none",
      "status": "COMPLETED",
      "source": null
    }
  }
}
```

## Get the impacts from cpu characteristics

In this query, we give some characteristics to describe the CPU. 

```bash
curl -X 'GET' \
  'http://localhost:5000/v1/component/cpu?verbose=false' \
  -H 'accept: application/json' \
  -d '{
      "core_units": 24,
      "family": "Skylake"
      }'
```

This query returns :

* The impacts of the CPU on the all life cycle


```json
{
  "gwp": {
    "manufacture": 23.8,
    "use": "not implemented",
    "unit": "kgCO2eq"
  },
  "pe": {
    "manufacture": 353,
    "use": "not implemented",
    "unit": "MJ"
  },
  "adp": {
    "manufacture": 0.02,
    "use": "not implemented",
    "unit": "kgSbeq"
  }
}
```