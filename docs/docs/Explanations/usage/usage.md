# Usage methodology

Usage impacts can be assessed at device or component level from usage configuration. 

Usage impacts are measured by multiplying a **[duration](duration.md)**, an **[impact factor](elec_factors.md)**, and an **[electrical consumption](elec_conso.md)** :

```impact = electrical_consumption * duration * impact_factor```

## Characteristics

| Name                         | Unit                         | Default value (default;min;max) | Description                                  | Example |
|------------------------------|------------------------------|---------------------------------|----------------------------------------------|---------|
| days_use_time                | None                         | One year (365 days)             | Number of days considered in the evaluation  | 2       |
| hours_use_time               | None                         | One year (8760 hours)           | Number of hours considered in the evaluation | 2       |
| years_use_time               | None                         | One year                        | Number of years considered in the evaluation | 2       |
| years_life_time              | None                         | Depends on the asset            | Lifespan of the element                      | 4       |
| usage_location               | trigram                      | EEE (EU27+1)                    | See [available country codes](countries.md)  | FRA     |
| hours_electrical_consumption | Watt/hour                    | None                            | Average electrical consumption per hour      | 120     |
| time_workload                | %workload or %time:%workload | 50%;0%;100%                     | See usage                                    | ..      |