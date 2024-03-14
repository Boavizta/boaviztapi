# Duration


Usage impacts are assessed for a specific time duration given by the user. The duration is given in hours.
When no duration is given, the impacts are measured for the all lifespans of the asset.

!!!info
    The duration is given by the user as a query parameter in the API request. If no duration is given, the API uses the lifespan of the device as the duration.

## Usage ratio

The usage ratio is the proportion of time the asset is used during the given duration. When an asset is always used, the usage ratio is 1. When a device is never used, the usage ratio is 0.

!!!info
    Users can give the usage ratio in the usage object. If no usage ratio is given, the API uses the usage ratio taken from the archetype.