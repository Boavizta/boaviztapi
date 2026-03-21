# Electrical impact factors

## User declaration

Users can give their own impact factors.

!!!warning
    We recommend using impact factors describing your national or regional electrical mix.
    An impact factor constructed from a market-based approach **should not be used**.

!!!info
    The factor is given in the `usage` object of the request.

## Boavizta's impact factors

Users can use the average impact factors per country available in BoaviztAPI.

!!!info
    Impact factors will depend on the `usage_location` defined by the user in usage object. By default, the average european mix is used.

`usage_location` are given in a trigram format, according to the [list of the available countries](countries.md).

!!!info
    Available countries can be retrieve using the API endpoint `/v1/utils/country_code`.

You can find bellow the data source and methodology used for each impact criteria.

## Electricity Maps Integration

You can use [Electricity Maps](https://app.electricitymaps.com/) to load live electricity impact factors by setting the `BOAVIZTA_ELECTRICITY_MAPS_API_KEY` environment variable to a valid API key for the Electricity Maps API.

Response data for each zone is cached in memory for 10 minutes, but this duration can be configured via the `BOAVIZTA_ELECTRICITY_MAPS_CACHE_EXPIRY_SECONDS` environment variable.

!!!info
    Electricity Maps currently only supports GWP as an impact factor. As a result, only the `gwp` factor of the _usage_ part of the impact will be based on Electricity Maps data.

!!!info
    Electricity Maps data is only available for given zones, and it does not provide any kind of global/regional averages. Therefore, the Boavizta location codes of `WOR` and `EEE` will also default to the default hard-coded factors.

### GWP - Global warming potential factor

_Source_ :

* For Europe (2019): [Quantification of the carbon intensity of electricity produced and used in Europe](https://www.sciencedirect.com/science/article/pii/S0306261921012149)
* For the rest of the world: [Ember Climate](https://ember-climate.org/data/data-explorer)

### PE - Primary energy factor

_Source_ :

PE impact factor are not available in open access.
We use the consumption of fossil resources per kwh (APDf/kwh) per country and extrapolate this consumption to renewable energy :

```PE/kwh = ADPf/kwh / (1-%RenewableEnergyInMix)```

* `%RenewableEnergyInMix` (2016): [List of countries by renewable electricity production](https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production) from IRENA
* `ADPf` (2011): [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)

### Other impact factors

| Criteria | Implemented | Source                                                   |
|----------|-------------|----------------------------------------------------------|
| adp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| gwppb    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| gwppf    | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| gwpplu   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ir       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| lu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| odp      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| pm       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| pocp     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| wu       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| mips     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| adpe     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| adpf     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ap       | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ctue     | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ctuh_c   | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ctuh_nc  | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| epf      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| epm      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
| ept      | yes         | [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/)    |
