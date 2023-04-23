## Impacts routes

The impact routes are used to retrieve the impacts of a given usage and configuration for a given device or component. They represent the main feature of the API.

### Query parameters

They all have the same query parameters. If no query parameters are provided, the default values will be used.

| Parameter        | Description                                                                                                                                        | Default                                                               | Example                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------|
| ```criteria```   | List the impact criteria you want the API to compute .All impacts criteria can be found here ```/v1/utils/impact_criteria```                       | ```criteria=gwp&criteria=pe&criteria=adp```                           | ```criteria=gwp```             |
| ```verbose```    | If set at true, the API will detail the data used in the assessment. See [verbose](../Explanations/verbose.md).                                    | ```allocation=true```                                                 |                                |
| ```allocation``` | The allocation method for embedded impacts. See [allocation](../Explanations/embedded_methodology.md#Allocation)                                   | ```allocation=TOTAL```                                                | ```allocation=TOTAL```         |
| ```archetype```  | The missing data will be completed from the chosen archetype. **Not implemented for cloud routes**. See [archetype](../Explanations/archetypes.md) | Default archetype for each asset can be set in the configuration file | ```archetype=compute_medium``` |

### GET

Requesting the route with a GET method will return the impacts with the values taken from the archetype.

| Method | Routes                         | Description                                         |  
|--------|--------------------------------|-----------------------------------------------------|  
| GET    | /v1/server                     | Retrieve the impacts of a server archetype          |  
| GET    | /v1/cloud                      | Retrieve the impacts of a cloud instance            |
| GET    | /v1/user_terminal/laptop       | Retrieve the impacts of a laptop                    |
| GET    | /v1/user_terminal/desktop      | Retrieve the impacts of a desktop (without screen)  |
| GET    | /v1/user_terminal/monitor      | Retrieve the impacts of a monitor (computer screen) |
| GET    | /v1/user_terminal/smartphone   | Retrieve the impacts of a smartphone                |
| GET    | /v1/user_terminal/tablet       | Retrieve the impacts of a tablet                    |
| GET    | /v1/user_terminal/television   | Retrieve the impacts of a television                |
| GET    | /v1/user_terminal/box          | Retrieve the impacts of a box                       |
| GET    | /v1/user_terminal/usb_stick    | Retrieve the impacts of a usb_stick                 |
| GET    | /v1/user_terminal/external_ssd | Retrieve the impacts of a external_ssd              |
| GET    | /v1/user_terminal/external_hdd | Retrieve the impacts of a external_hdd              |
| GET    | /v1/component/cpu              | Retrieve the impacts of a cpu                       |
| GET    | /v1/component/ssd              | Retrieve the impacts of a ssd                       |
| GET    | /v1/component/ram              | Retrieve the impacts of a ram                       |
| GET    | /v1/component/hdd              | Retrieve the impacts of a hdd                       |
| GET    | /v1/component/motherboard      | Retrieve the impacts of a motherboard               |
| GET    | /v1/component/power_supply     | Retrieve the impacts of a power_supply              |
| GET    | /v1/component/case             | Retrieve the impacts of a case                      |

### POST

Requesting the route with a POST method will return the impacts with the values taken from the body. Missing values will be taken from the archetype or set by default.
The format section of the documentation details the format of the body for each route.

| Method   | Routes                         | Description                                                                             |  
|----------|--------------------------------|-----------------------------------------------------------------------------------------|  
| POST     | /v1/server                     | Retrieve the impacts of a given usage and configuration for a server                    |  
| POST     | /v1/cloud                      | Retrieve the impacts of a given usage for a cloud instance                              |
| POST     | /v1/user_terminal/laptop       | Retrieve the impacts of a given usage and configuration for a laptop                    |
| POST     | /v1/user_terminal/desktop      | Retrieve the impacts of a given usage and configuration for a desktop (without screen)  |
| POST     | /v1/user_terminal/monitor      | Retrieve the impacts of a given usage and configuration for a monitor (computer screen) |
| POST     | /v1/user_terminal/smartphone   | Retrieve the impacts of a given usage and configuration for a smartphone                |
| POST     | /v1/user_terminal/tablet       | Retrieve the impacts of a given usage and configuration for a tablet                    |
| POST     | /v1/user_terminal/television   | Retrieve the impacts of a given usage and configuration for a television                |
| POST     | /v1/user_terminal/box          | Retrieve the impacts of a given usage and configuration for a box                       |
| POST     | /v1/user_terminal/usb_stick    | Retrieve the impacts of a given usage and configuration for a usb_stick                 |
| POST     | /v1/user_terminal/external_ssd | Retrieve the impacts of a given usage and configuration for a external_ssd              |
| POST     | /v1/user_terminal/external_hdd | Retrieve the impacts of a given usage and configuration for a external_hdd              |
| POST     | /v1/component/cpu              | Retrieve the impacts of a given usage and configuration for a cpu                       |
| POST     | /v1/component/ssd              | Retrieve the impacts of a given usage and configuration for a ssd                       |
| POST     | /v1/component/ram              | Retrieve the impacts of a given usage and configuration for a ram                       |
| POST     | /v1/component/hdd              | Retrieve the impacts of a given usage and configuration for a hdd                       |
| POST     | /v1/component/motherboard      | Retrieve the impacts of a given usage and configuration for a motherboard               |
| POST     | /v1/component/power_supply     | Retrieve the impacts of a given usage and configuration for a power_supply              |
| POST     | /v1/component/case             | Retrieve the impacts of a given usage and configuration for a case                      |

## Consumption profile routes

| Method | Routes                       | parameters      | Description                                                                                                                          |  
|--------|------------------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------|  
| POST   | /v1/consumption_profile/cpu  | ```verbose```   | Retrieve the consumption profile of a given CPU. See [get started with consumption profiles](../Explanations/consumption_profile.md) |

## Utils routes

Utils routes are used to retrieve the list of possible values for some parameters, to retrieve the list of archetypes for a given asset or to use some specific features.

| Method | Routes                        | parameters     | Description                                                        |  
|--------|-------------------------------|----------------|--------------------------------------------------------------------|  
| GET    | /v1/server/archetypes         |                | Get all available server archetype                                 |
| GET    | /v1/cloud/all_instances       | ```provider``` | Get all available cloud instances for a given provider             |
| GET    | /v1/cloud/all_providers       |                | Get all available cloud providers                                  |
| GET    | /v1/user_terminal/archetypes  | ```name```     | Get all available archetype for a given component name             |
| GET    | /v1/component/archetypes      | ```name```     | Get all available archetype for a end user terminal name           |
| GET    | /v1/utils/country_code        |                | Get all available country code associated to its country name      |
| GET    | /v1/utils/cpu_model_range     |                | Get all available model_range                                      |
| GET    | /v1/utils/ssd_manufacturer    |                | Get all available ssd manufacturer                                 |
| GET    | /v1/utils/ram_manufacturer    |                | Get all available ram manufacturer                                 |
| GET    | /v1/utils/case_type           |                | Get all available case type                                        |
| GET    | /v1/utils/name_to_cpu         | ```cpu_name``` | Get a description of a CPU from its name                           |
| GET    | /v1/utils/cpu_name            |                | Get all available cpu name                                         |
| GET    | /v1/utils/impact_criteria     |                | Get all available impact criteria  (name, code, description, unit) |