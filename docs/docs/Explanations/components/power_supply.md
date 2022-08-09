# Power supply

## Characteristics

| Name               | Unit | Default value | Description                 | Example |
|--------------------|------|---------------|-----------------------------|---------|
| units              | None | 1             | power supply quantity       | 2       |
| usage              | None | See Usage     | See usage                   | ..      |
| unit_weight        | kg   | 2.99          | weight of the power supply  | 5       |

## Manufacture impact

<h6>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>units</sub> x psu<sub>unit<sub>weight</sub></sub> x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h6>

With :

| Constant           | Unit       | Value    |
|--------------------|------------|----------|
| psumanuf_weightgwp | kgCO2eq/kg | 24.30    |
| psumanuf_weightadp | kgSbeq/kg  | 8.30E-03 |
| psumanuf_weightpe  | MJ/kg      | 352.00   |

## Usage impact

Only power consumption is implemented. 
This shouldn't be used since the electricity consume by a power supply is consume on behalf of other components.