# SERVER - BOTTOM-UP METHODOLOGY

## Documentation

The bottom-up methodology measures impacts of devices (only servers for now) by aggregating the impact of each of its component. 
The bottom-up measure only the impact of the **manufacture**

### Variable components impacts

The impact of variable components are proportional to the die size of their chips

* CPU
* RAM
* DISK (SSD)


### Fixed components impacts

The impact of fixed component are set by default

* DISK (HDD)
* MOTHERBOARD
* POWER SUPPLY
* MANUFACTURE ASSEMBLY


## Ressources

[Boavizta server impact measurement methodology](https://boavizta.cmakers.io/blog/numerique-et-environnement-comment-evaluer-l-empreinte-de-la-fabrication-d-un-serveur-au-dela-des-emissions-de-gaz-a-effet-de-se?token=2112aecb183b1b5d27e137abc61e0f0d39fabf99)


## Details by components

### CPU

<h6>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>units<sub></sub></sub> x ( ( cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0,491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + cpu<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

with:

|Constante|Unité|Valeur|
|--- |--- |--- |
|cpudiesize|cm2|**|
|cpumanuf_diegwp|kgCO2eq/cm2|1.97|
|cpumanuf_dieadp|kgSbeq/cm2|5.80E-07|
|cpumanuf_diepe|MJ/cm2|26.50|
|cpumanuf_basegwp|kgCO2eq|9.14|
|cpumanuf_baseadp|kgSbeq|2.04E-02|
|cpumanuf_basepe|MJ|156.00|

 ** The value is given by the user or found if CPU technical information are given or set by default

### RAM

<h6>ram<sub>manuf<sub><em>criteria</em></sub></sub> = ram<sub>units</sub> x ( ( ram<sub>size</sub> / ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + ram<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With

|Constante|Unité|Valeur|
|--- |--- |--- |
|ramdensity|GB/cm2|**|
|rammanuf_diegwp|kgCO2eq/cm2|2.20|
|rammanuf_dieadp|kgSbeq/cm2|6.30E-05|
|rammanuf_diepe|MJ/cm2|27.30|
|rammanuf_basegwp|kgCO2eq|5.22|
|rammanuf_baseadp|kgSbeq|1.69E-03|
|rammanuf_basepe|MJ|74.00|


** The value is given by the user or found if SSD technical information are given or set by default


### SSD

<h6>ssd<sub>manuf<sub><em>criteria</em></sub></sub> = ssd<sub>units</sub> x ( ( ssd<sub>size</sub> / ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + ssd<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With:

|Constante|Unité|Valeur|
|--- |--- |--- |
|ssddensity|GB/cm2|**|
|ssdmanuf_diegwp|kgCO2eq/cm2|2.20|
|ssdmanuf_dieadp|kgSbeq/cm2|6.30E-05|
|ssdmanuf_diepe|MJ/cm2|27.30|
|ssdmanuf_basegwp|kgCO2eq|6.34|
|ssdmanuf_baseadp|kgSbeq|5.63E-04|
|ssdmanuf_basepe|MJ|76.90|

** The value is given by the user or found if SSD technical information are given or set by default

### HDD

<h6>hdd<sub>manuf<sub><em>criteria</em></sub></sub> = hdd<sub>units</sub> x hdd<sub>manuf_unit<sub><em>criteria</em></sub></sub></h6>

With:

|Constante|Unité|Valeur|
|--- |--- |--- |
|hddmanuf_unitgwp|kgCO2eq|31.10|
|hddmanuf_unitadp|kgSbeq|2.50E-04|
|hddmanuf_unitpe|MJ|276.00|


### Power supply

<h6>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>units</sub> x psu<sub>unit<sub>weight</sub></sub> x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h6>

With :

|Constante|Unité|Valeur|
|--- |--- |--- |
|psumanuf_weightgwp|kgCO2eq/kg|24.30|
|psumanuf_weightadp|kgSbeq/kg|8.30E-03|
|psumanuf_weightpe|MJ/kg|352.00|


### Enclosure

*Rack server:*

<h6>enclosure<sub>manuf<sub><em>criteria</em></sub></sub> = rack<sub>manuf<sub><em>criteria</em></sub></sub></h6>

*Blade server:*

<h6>enclosure<sub>manuf<sub><em>criteria</em></sub></sub> = blade<sub>manuf<sub><em>criteria</em></sub></sub> + blade_enclosure<sub>manuf<sub><em>criteria</em></sub></sub> / 16</h6>

With :

|Constante|Unité|Valeur|
|--- |--- |--- |
|rackmanufgwp|kgCO2eq|150|
|rackmanufadp|kgSbeq|2.02E-02|
|rackmanufpe|MJ|2 200.00|
|blademanufgwp|kgCO2eq|30.90|
|blademanufadp|kgSbeq|6.72E-04|
|blademanufpe|MJ|435.00|
|blade_enclosuremanufgwp|kgCO2eq|880.00|
|blade_enclosuremanufadp|kgSbeq|4.32E-01|
|blade_enclosuremanufpe|MJ|12 700.00|


##For the overall server

<h6>server<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>manuf<sub><em>criteria</em></sub></sub> + ram<sub>manuf<sub><em>criteria</em></sub></sub> + ssd<sub>manuf<sub><em>criteria</em></sub></sub>+ hdd<sub>manuf<sub><em>criteria</em></sub></sub> + motherboard<sub>manuf<sub><em>criteria</em></sub></sub> + psu<sub>manuf<sub><em>criteria</em></sub></sub> + enclosure<sub>manuf<sub><em>criteria</em></sub></sub> + assembly<sub>manuf<sub><em>criteria</em></sub></sub></h6>

With :

|Constante|Unité|Valeur|
|--- |--- |--- |
|motherboardmanufgwp|kgCO2eq|66.10|
|motherboardmanufadp|kgSbeq|3.69E-03|
|motherboardmanufpe|MJ|836.00|
|assemblymanufgwp|kgCO2eq|6.68|
|assemblymanufadp|kgSbeq|1.41E-06|
|assemblymanufpe|MJ|68.60|
