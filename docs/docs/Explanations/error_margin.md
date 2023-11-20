# Error margin

!!!warning
    Feature still in development

!!!info
    All environmental impacts are returned with a min and max values.

## Error margin from the impact factors 

Error can be caused by the impact factors used in the calculation since those impact factors are not specific to the process you are computing. For example, the impact factor of the electricity consumption is based on the average electricity consumption of a country over a year. In reality, the electricity mix and its associated impacts vary a lot during a year.

!!!warning
    We do not take into account the error margin from the impact factors in the API.

## Error margin from incomplete user input 

Error can also be caused by incomplete user input. This type of error margins are taken into account.

### Error margin from default values

Error margins are set when ```DEFAULT``` values are used. For example, if you do not provide the usage location of a device, the API will use the default usage location of the device.In this case we set a minimal (min) and maximal value (max) based on the available usage location and compute the impact with the minimal and maximal value to report a min and max impacts values.

### Error margin from [archetype](archetypes.md) values

Error margins are set when ```ARCHETYPE``` values are used. For example, if you do not provide any information on your CPU, we will use the value of the attribute taken from the archetype. If the archetype provide a min and a max value for this specific attribute, those values will be used to compute min and max impacts values.


## Rounding

Impact values are rounded depending on the distance between min and max values. The bigger the difference, the more aggressive the rounding.
To adapt the intensity of the rounding, we use an uncertainty percentage which can be set in configuration file. The default value is 10%. The lower the uncertainty percentage, the lower aggressive the rounding.

You can set a minimal and maximal significant digit for the rounding in the configuration file.