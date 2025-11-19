from fastapi import HTTPException

from boaviztapi.service.costs_provider import ElectricityCostsProvider


def check_alpha3_in_electricity_prices(alpha3: str):
    if alpha3 not in [c.alpha_3 for c in ElectricityCostsProvider.get_eic_countries()]:
        raise ValueError("This ISO 3166-1 alpha3 code is not supported!")
    return alpha3

def check_zone_code_in_electricity_maps(zone: str):
    if zone not in [c.zone_code for c in ElectricityCostsProvider.get_eic_countries()]:
        print("test")
        raise ValueError("This zone code is not supported!")
    return zone
