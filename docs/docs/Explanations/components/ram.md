# RAM

## Characteristics

| Name             | Unit   | Default value | Description                           | Example |
|------------------|--------|---------------|---------------------------------------|---------|
| units            | None   | 1             | RAM strip quantity                    | 2       |
| usage            | None   | See Usage     | See usage                             | ..      |
| capacity         | Go     | 32            | Capacity of a ram strip               | 12      |
| density          | cm2/Go | 0.625         | Size of the die per Go of a ram strip | 1.25    |
| process          | nm     | None          | Engraving process (Architecture)      | 25      |
| manufacturer     | None   | None          | Name of the ram manufacturer          | Samsung |
| model            | None   | None          | ..                                    | ..      |


## Complete

**The following variables can be [completed](complete.md)**

### density

if ```process``` or/and ```manufacturer``` are given, ```density``` can be retrieved from a fuzzy matching on our ram repository.
If several ram matches the given ```process``` or/and ```manufacturer``` the maximizing value is given (in terms of impacts).

## Manufacture impact

<h6>ram<sub>manuf<sub><em>criteria</em></sub></sub> = ram<sub>units</sub> x ( ( ram<sub>size</sub> / ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + ram<sub>manuf_base<sub><em>criteria</em></sub></sub> )</h6>

With

| Constant          | Units       | Value      |
|-------------------|-------------|------------|
| rammanuf_diegwp   | kgCO2eq/cm2 | 2.20       |
| rammanuf_dieadp   | kgSbeq/cm2  | 6.30E-05   |
| rammanuf_diepe    | MJ/cm2      | 27.30      |
| rammanuf_basegwp  | kgCO2eq     | 5.22       |
| rammanuf_baseadp  | kgSbeq      | 1.69E-03   |
| rammanuf_basepe   | MJ          | 74.00      |

## Usage impact

Only power consumption is implemented.