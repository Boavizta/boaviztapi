available_countries_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "zone_code": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "subdivision_name": {
                "type": "string"
            },
            "EIC_code": {
                "type": "string"
            },
            "alpha_3": {
                "type": "string"
            }
        },
        "required": [
            "zone_code",
            "name",
            "subdivision_name",
            "EIC_code",
            "alpha_3"
        ]
    }
}

electricity_prices_elecmaps_latest_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "zone": {
            "type": "string"
        },
        "datetime": {
            "type": "string"
        },
        "createdAt": {
            "type": "string"
        },
        "updatedAt": {
            "type": "string"
        },
        "value": {
            "type": "number"
        },
        "unit": {
            "type": "string"
        },
        "source": {
            "type": "string"
        },
        "temporalGranularity": {
            "type": "string"
        }
    },
    "required": [
        "zone",
        "datetime",
        "createdAt",
        "updatedAt",
        "value",
        "unit",
        "source",
        "temporalGranularity"
    ]
}

electricity_carbon_intensity_elecmaps_latest_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "zone": {
            "type": "string"
        },
        "carbonIntensity": {
            "type": "number"
        },
        "datetime": {
            "type": "string"
        },
        "updatedAt": {
            "type": "string"
        },
        "createdAt": {
            "type": "string"
        },
        "emissionFactorType": {
            "type": "string"
        },
        "isEstimated": {
            "type": "boolean"
        },
        "estimationMethod": {
            "type": "string"
        },
        "temporalGranularity": {
            "type": "string"
        }
    },
    "required": [
        "zone",
        "carbonIntensity",
        "datetime",
        "updatedAt",
        "createdAt",
        "emissionFactorType",
        "isEstimated",
        "estimationMethod",
        "temporalGranularity"
    ]
}


