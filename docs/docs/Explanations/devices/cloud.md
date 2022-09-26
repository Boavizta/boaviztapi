# Cloud instances

## Characteristics

| Name       | Unit | Default value   | Description           | Example |
|------------|------|-----------------|-----------------------|---------|
| units      | None | 1               | power supply quantity | 2       |
| usage      | None | See Cloud Usage | See cloud usage       | ..      |


## Manufacture impact

Manufacture impacts of cloud instances correspond to the impact of the physical [server](server.md) hosting the instance divided by the number of instances hosted on the server.

```CloudInstancemanufcriteria = servermanufcriteria / instance_per_server```

Components configuration are never sent by the user but pre-recorded as an [archetype](../archetypes.md).

## Usage impact

Usage impact of cloud instance are measured only from its [consumption profile](../consumption_profile.md).

As for manufacture, usage impact for a physical server are divided into the number of instances hosted by the server.

## Consumption profile

We use the same process as described for the servers. 
