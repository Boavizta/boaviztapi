# Electrical impact factors

## User declaration

Users can give their own impact factors.

_Note : We recommend to use impact factors describing your national electricity mix. An impact factor constructed from a market-based approach **should not be used**._


## Boavizta's impact factors

Users can use the average impact factors per country available in BoaviztAPI. 

Impact factors will depend on the `usage_location` defined by the user. By default, the average european mix is used.

`usage_location` are given in a trigram format, according to the [list of the available countries](countries.md).

You can find bellow the data source and methodology used for each impact criteria.

### GWP - Global warming potential factor

_Source_ : 

* For Europe (2019): [Quantification of the carbon intensity of electricity produced and used in Europe](https://www.sciencedirect.com/science/article/pii/S0306261921012149)
* For the rest of the world (2011): [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/) 


### PE - Primary energy factor

_Source_ : 

PE impact factor are not available in open access. 
We use the consumption of fossil resources per kwh (APDf/kwh) per country and extrapolate this consumption to renewable energy :

```PE/kwh = ADPf/kwh / (1-%RenewableEnergyInMix)```

* `%RenewableEnergyInMix` (2016): [List of countries by renewable electricity production](https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production) from IRENA
* `ADPf` (2011): [Base IMPACTS® ADEME](https://base-impacts.ademe.fr/) 

### ADP - Abiotic Depletion Potential

_Source_ :

* ADP (2011) : BASE IMPACT ADEME 

