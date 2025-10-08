available_countries_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "EIC_code": {
        "type": "string"
      },
      "country_name": {
        "type": "string"
      },
      "ISO3 Code": {
        "type": "string"
      }
    },
    "required": [
      "EIC_code",
      "country_name",
      "ISO3 Code"
    ]
  }
}