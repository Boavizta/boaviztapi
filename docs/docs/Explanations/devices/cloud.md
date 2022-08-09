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



## Resources

[AWS server configuration - Benjamin Davy for teads](https://medium.com/teads-engineering/evaluating-the-carbon-footprint-of-a-software-platform-hosted-in-the-cloud-e716e14e060c)