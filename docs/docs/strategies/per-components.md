#Components

## CPU

<h6>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = cpu<sub>units<sub></sub></sub> x ( ( cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0,491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + cpu<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

with:

|Constante|Unité|Valeur|
|--- |--- |--- |
|cpumanuf_diegwp|kgCO2eq/cm2|1.97|
|cpumanuf_dieadp|kgSbeq/cm2|5.80E-07|
|cpumanuf_diepe|MJ/cm2|26.50|
|cpumanuf_basegwp|kgCO2eq|9.14|
|cpumanuf_baseadp|kgSbeq|2.04E-02|
|cpumanuf_basepe|MJ|156.00|

**The following variables can be [smart-complete](../concepts/smart-complete.md)**

* cpu<sub>units<sub></sub></sub>
* cpu<sub>core<sub>units</sub></sub>
* cpu<sub>diesize</sub>


## RAM

<h6>ram<sub>manuf<sub><em>criteria</em></sub></sub> = ram<sub>units</sub> x ( ( ram<sub>size</sub> / ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + ram<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With

|Constante|Unité|Valeur|
|--- |--- |--- |
|rammanuf_diegwp|kgCO2eq/cm2|2.20|
|rammanuf_dieadp|kgSbeq/cm2|6.30E-05|
|rammanuf_diepe|MJ/cm2|27.30|
|rammanuf_basegwp|kgCO2eq|5.22|
|rammanuf_baseadp|kgSbeq|1.69E-03|
|rammanuf_basepe|MJ|74.00|

**The following variables can be [smart-complete](../concepts/smart-complete.md)**

* ram<sub>units</sub>
* ram<sub>density</sub>
* ram<sub>size</sub>


## SSD

<h6>ssd<sub>manuf<sub><em>criteria</em></sub></sub> = ssd<sub>units</sub> x ( ( ssd<sub>size</sub> / ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + ssd<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With:

|Constante|Unité|Valeur|
|--- |--- |--- |
|ssdmanuf_diegwp|kgCO2eq/cm2|2.20|
|ssdmanuf_dieadp|kgSbeq/cm2|6.30E-05|
|ssdmanuf_diepe|MJ/cm2|27.30|
|ssdmanuf_basegwp|kgCO2eq|6.34|
|ssdmanuf_baseadp|kgSbeq|5.63E-04|
|ssdmanuf_basepe|MJ|76.90|

**The following variables can be [smart-complete](../concepts/smart-complete.md)**

* ssd<sub>units</sub>
* ssd<sub>size</sub>
* ssd<sub>density</sub>


## HDD

<h6>hdd<sub>manuf<sub><em>criteria</em></sub></sub> = hdd<sub>units</sub> x hdd<sub>manuf_unit<sub><em>criteria</em></sub></sub></h6>

With:

|Constante|Unité|Valeur|
|--- |--- |--- |
|hddmanuf_unitgwp|kgCO2eq|31.10|
|hddmanuf_unitadp|kgSbeq|2.50E-04|
|hddmanuf_unitpe|MJ|276.00|

**The following variables can be [smart-complete](../concepts/smart-complete.md)**

* hdd<sub>units</sub>


## Power supply

<h6>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>units</sub> x psu<sub>unit<sub>weight</sub></sub> x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h6>

With :

|Constante|Unité|Valeur|
|--- |--- |--- |
|psumanuf_weightgwp|kgCO2eq/kg|24.30|
|psumanuf_weightadp|kgSbeq/kg|8.30E-03|
|psumanuf_weightpe|MJ/kg|352.00|

**The following variables can be [smart-complete](../concepts/smart-complete.md)**

* psu<sub>units</sub>
* psu<sub>unit<sub>weight</sub>

## Enclosure

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

**Blade servers are choosen by default if the enclosure isn't specified**


## Motherboard

<h6>motherboard<sub>manuf<sub><em>criteria</em></sub></sub></h6>


|Constante|Unité|Valeur|
|--- |--- |--- |
|motherboardmanufgwp|kgCO2eq|66.10|
|motherboardmanufadp|kgSbeq|3.69E-03|
|motherboardmanufpe|MJ|836.00|


## Assembly


<h6>assembly<sub>manuf<sub><em>criteria</em></sub></sub></h6>

|Constante|Unité|Valeur|
|--- |--- |--- |
|assemblymanufgwp|kgCO2eq|6.68|
|assemblymanufadp|kgSbeq|1.41E-06|
|assemblymanufpe|MJ|68.60|