# Usage methodology

Usage impacts can be measured at device or component level from usage configuration. 

Usage impacts are measured by multiplying a **[duration](duration.md)**, an **[impact factor](elec_factors.md)**, and an **[electrical consumption](elec_conso.md)** :

```impact = electrical_consumption * duration * impact_factor```

## Characteristics

### General usage

| Name                         | Unit                           | Default value         | Description                                  | Example |
|------------------------------|--------------------------------|-----------------------|----------------------------------------------|---------|
| days_use_time                | None                           | One year (365 days)   | Number of days considered in the evaluation  | 2       |
| hours_use_time               | None                           | One year (8760 hours) | Number of hours considered in the evaluation | 2       |
| years_use_time               | None                           | One year              | Number of years considered in the evaluation | 2       |
| years_life_time              | None                           | 3                     | Lifespan of the element                      | 4       |
| usage_location               | trigram                        | EEE (EU27+1)          | See [available country codes](countries.md)  | FRA     |
| hours_electrical_consumption | Watt/hour                      | None                  | Average electrical consumption per hour      | 120     |
| time_workload                | {%workload or %time:%workload} | 50%                   | See usage                                    | ..      |


### Server usage

In addition to the parameters from the above table, you can use the following:

| Name                    | Unit | Default value | Description                                                         | Example |
|-------------------------|------|---------------|---------------------------------------------------------------------|---------|
| other_consumption_ratio | None | 0.33          | Power consumption ratio of other components relative to RAM and CPU | 0.2     |

### Cloud usage

In addition to the parameters from both tables above, you can use the following:

| Name                  | Unit       | Default value | Description                                    | Example |
|-----------------------|------------|---------------|------------------------------------------------|---------|
| instance_per_server   | None       | 1             | See usage                                      | 10      |
| years_life_time       | Non        | 2             | Lifespan of the element                        | 2       |
