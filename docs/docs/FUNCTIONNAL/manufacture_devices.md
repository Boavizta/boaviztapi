# Manufacture impacts per devices

Manufacture impacts of a component are the aggregation of each of the manufacture impacts of its components.


## Server

<h6>server<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>manuf<sub><em>criteria</em></sub></sub> + ram<sub>manuf<sub><em>criteria</em></sub></sub> + ssd<sub>manuf<sub><em>criteria</em></sub></sub>+ hdd<sub>manuf<sub><em>criteria</em></sub></sub> + motherboard<sub>manuf<sub><em>criteria</em></sub></sub> + psu<sub>manuf<sub><em>criteria</em></sub></sub> + enclosure<sub>manuf<sub><em>criteria</em></sub></sub> + assembly<sub>manuf<sub><em>criteria</em></sub></sub></h6>

**The following component are set be default ** :

* Motherboard
* Assembly

**The following component are [smart-complete](smart-complete.md) if not given by the user ** :

* CPU
* RAM
* POWER-SUPPLY
* SSD (TO CHANGE)
* ENCLOSURE (Rack by default)

### Resources

[Server manufacture impact - Boavizta](https://www.boavizta.org/blog/empreinte-de-la-fabrication-d-un-serveur)

## Cloud instance

Manufacture impacts of cloud instances correspond to the impact of the physical server hosting the instance divided by the number of instances hosted on the server.

<h6>CloudInstance<sub>manuf<sub><em>criteria</em></sub></sub> = server<sub>manuf<sub><em>criteria</em></sub></sub> / instance_per_server </h6>

Components configuration are never sent by the user but pre-recorded as an [archetype](archetypes.md).

### Resources

[AWS server configuration - Benjamin Davy for teads](https://medium.com/teads-engineering/evaluating-the-carbon-footprint-of-a-software-platform-hosted-in-the-cloud-e716e14e060c)