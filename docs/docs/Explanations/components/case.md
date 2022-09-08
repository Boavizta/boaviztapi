# Case or Enclosure

## Characteristics

| Name       | Unit | Default value | Description                       | Example |
|------------|------|---------------|-----------------------------------|---------|
| units      | None | 1             | power supply quantity             | 2       |
| usage      | None | See Usage     | See usage                         | ..      |
| case_type  | None | rack          | Type of enclosure (blade or rack) | blade   |

## Manufacture impact

*For rack server:*

<h6>enclosure<sub>manuf<sub><em>criteria</em></sub></sub> = rack<sub>manuf<sub><em>criteria</em></sub></sub></h6>

*For blade server:*

<h6>enclosure<sub>manuf<sub><em>criteria</em></sub></sub> = blade<sub>manuf<sub><em>criteria</em></sub></sub> + blade_enclosure<sub>manuf<sub><em>criteria</em></sub></sub> / 16</h6>

With :

| Constant                | Unit    | Value     |
|-------------------------|---------|-----------|
| rackmanufgwp            | kgCO2eq | 150       |
| rackmanufadp            | kgSbeq  | 2.02E-02  |
| rackmanufpe             | MJ      | 2 200.00  |
| blademanufgwp           | kgCO2eq | 30.90     |
| blademanufadp           | kgSbeq  | 6.72E-04  |
| blademanufpe            | MJ      | 435.00    |
| blade_enclosuremanufgwp | kgCO2eq | 880.00    |
| blade_enclosuremanufadp | kgSbeq  | 4.32E-01  |
| blade_enclosuremanufpe  | MJ      | 12 700.00 |

## Usage impact

Only power consumption is implemented. In most cases, enclosure doesn't consume electricity.