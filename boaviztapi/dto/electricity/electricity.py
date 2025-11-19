from typing import Optional

from boaviztapi.dto import BaseDTO


class Country(BaseDTO):
    """
    Country schema class used by Electricity APIs to return location-based data

    Attributes:
        zone_code: ElectricityMaps zone code for the zone defined by the API (used as a unique identifier)
        name: Country name as defined by ISO 3166-1
        subdivision_name: Country subdivision as defined by ISO 3166-2
        EIC_code: Energy Identification Code (EIC) - available for European countries only
        alpha_3: ISO 3166-1 alpha-3 country code
    """
    zone_code: str
    name: str
    subdivision_name: str
    EIC_code: Optional[str] = None
    alpha_3: str

