# Consumption profile

!!!warning
    Error margins are not yet implemented for the consumption profile.

A consumption profile is a continuous function which links a workload with an electrical consumption :
```consumption_profile(workload) = power_consumption```

The completion strategy of the consumption profile is specified for each device or component when implemented.

You will find the details of each of the consumption profiles in the respective components and device pages. Consumption profile are implemented for :

* [CPU](components/cpu.md)
* [RAM](components/ram.md)
* [Server](devices/server.md)
* [Cloud instances](services/cloud.md)


## Dataset

The consumption profiles are produced empirically from spot measurements at different workload levels on different architectures. We rely on the data described here:

* [AWS server configuration - Benjamin Davy for teads](https://medium.com/teads-engineering/evaluating-the-carbon-footprint-of-a-software-platform-hosted-in-the-cloud-e716e14e060c)

* [Energizta](https://github.com/Boavizta/Energizta) project aims to build a collaborative database to refine the consumption profiles usable in the API.

