# Electrical impact factors

## User declaration

Users can give their own impact factors.

_Note : We recommend the use of an impact factor describing the national electricity mix. An impact factor constructed from a market-based approach should not be used._


## Boavizta's impact factors

Users can use the average impact factors per country available in BoaviztAPI. 

Impact factors will depend on the `usage_location`. `usage_location` can be defined by the user. By default, the average european mix is used.

`usage_location` are given in a trigram format. You can find the list of the available countries [here](countries.md).

You can find bellow the data source and methodology used.


### GWP - Global warming potential factor

_Source_ : 

* For Europe (2019) : https://www.sciencedirect.com/science/article/pii/S0306261921012149
* For the rest of the world (2011) : BASE IMPACT ADEME 


### PE - Primary energy factor

_Source_ : 

PE impact factor are not available in open access. 
We use the consumption of fossil resources per kwh (APDf/kwh) per country and extrapolate this consumption to renewable energy :

```PE/kwh = ADPf/kwh / (1-%RenewableEnergyInMix)```

* %RenewableEnergyInMix (2016) : 'https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production from IRENA
* ADPf (2011): BASE IMPACT ADEME

### ADP - Abiotic Depletion Potential

_Source_ :
* ADP (2011) : BASE IMPACT ADEME 

