import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_laptop():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post('/v1/terminal/laptop?verbose=false&criteria=ir', json={})

    assert res.status_code == 200
    assert res.json() == {'impacts': {'ir': {'description': 'Emissions of radionizing substances',
                                             'embedded': {'max': 73.6,
                                                          'min': 73.6,
                                                          'value': 73.6,
                                                          'warnings': ['Generic data used for impact '
                                                                       'calculation.']},
                                             'unit': 'kg U235 eq.',
                                             'use': {'max': 3446.0, 'min': 0.05643, 'value': 900.0}}}}


@pytest.mark.asyncio
async def test_desktop():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/desktop?verbose=false&criteria=lu')

    assert res.status_code == 200
    assert res.json() == {'impacts': {'lu': {'description': 'Land use',
                                             'embedded': {'max': -101.0,
                                                          'min': -101.0,
                                                          'value': -101.0,
                                                          'warnings': ['Generic data used for impact '
                                                                       'calculation.']},
                                             'unit': 'No dimension',
                                             'use': 'not implemented'}}}


@pytest.mark.asyncio
async def test_smartphone():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/smartphone?verbose=true')

    assert res.status_code == 200
    assert res.json() == {"impacts": {"gwp": {"unit": "kgCO2eq", "description": "Total climate change",
                                              "embedded": {"value": 84.0, "min": 84.0, "max": 84.0,
                                                           "warnings": ["Generic data used for impact calculation."]},
                                              "use": {"value": 2.0, "min": 0.07555, "max": 17.74}},
                                      "adp": {"unit": "kgSbeq", "description": "Use of minerals and fossil ressources",
                                              "embedded": "not implemented",
                                              "use": {"value": 4e-07, "min": 4.336e-08, "max": 5.235e-06}},
                                      "pe": {"unit": "MJ", "description": "Consumption of primary energy",
                                             "embedded": "not implemented",
                                             "use": {"value": 100.0, "min": 0.0427, "max": 9227.0}}},
                          "verbose": {"duration": {"value": 21900.0, "unit": "hours"},
                                      "avg_power": {"value": 1.0, "status": "ARCHETYPE", "unit": "W", "min": 0.5,
                                                    "max": 3.0}, "usage_location": {"value"
                                                                                    : "EEE", "status": "DEFAULT",
                                                                                    "unit": "CodSP3 - NCS Country Codes - NATO"},
                                      "use_time_ratio": {"value": 0.3, "status": "ARCHETYPE", "unit": "/1", "min": 0.3,
                                                         "max": 0.3},
                                      "hours_life_time": {"value": 21900.0, "status": "ARCHETYPE", "unit": "hours",
                                                          "min": 21900.0, "max": 21900.0},
                                      "gwp_factor": {"value": 0.38, "status": "DEFAULT", "unit": "kg CO2eq/kWh",
                                                     "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \nAverage of 27 european countries",
                                                     "min": 0.023, "max": 0.9},
                                      "adp_factor": {"value": 6.42e-08, "status": "DEFAULT", "unit": "kg Sbeq/kWh",
                                                     "source": "ADEME Base IMPACTS ®", "min": 1.32e-08,
                                                     "max": 2.656e-07},
                                      "pe_factor": {"value": 12.874, "status": "DEFAULT", "unit": "MJ/kWh",
                                                    "source": "ADPf / (1-%renewable_energy)", "min": 0.013,
                                                    "max": 468.15}, "units": {"value": 1, "status": "ARCHETYPE", "min":
                                  1, "max": 1}}}


@pytest.mark.asyncio
async def test_box():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/box?verbose=true&criteria=adpe')

    assert res.status_code == 200
    assert res.json() == {"impacts": {"adpe": {"unit": "kg SB eq.", "description": "Use of mineral and metal resources",
                                               "embedded": {"value": 4.41e-05, "min": 4.41e-05, "max": 4.41e-05,
                                                            "warnings": ["Generic data used for impact calculation."]},
                                               "use": {"value": 3e-05, "min": 2.891e-06, "max": 0.0002327}}},
                          "verbose": {"duration": {"value": 43800.0, "unit": "hours"},
                                      "avg_power": {"value": 10.0, "status": "ARCHETYPE", "unit": "W", "min": 5.0,
                                                    "max": 20.0},
                                      "usage_location": {"value": "EEE", "status": "DEFAULT",
                                                         "unit": "CodSP3 - NCS Country Codes - NATO"},
                                      "use_time_ratio": {"value": 1.0, "status": "ARCHETYPE", "unit": "/1", "min": 1.0,
                                                         "max": 1.0},
                                      "hours_life_time": {"value": 43800.0, "status": "ARCHETYPE", "unit": "hours",
                                                          "min": 43800.0, "max": 43800.0},
                                      "adpe_factor": {"value": 6.42e-08, "status": "DEFAULT", "unit": "kg Sbeq/kWh",
                                                      "source": "ADEME Base IMPACTS ®", "min": 1.32e-08,
                                                      "max": 2.656e-07},
                                      "units": {"value": 1, "status": "ARCHETYPE", "min": 1, "max": 1}}}


@pytest.mark.asyncio
async def test_tv_archetype_perso():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/television?verbose=true&criteria=adpe&archetype=tv-perso')

    assert res.status_code == 200
    assert res.json() == {"impacts": {"adpe": {"unit": "kg SB eq.", "description": "Use of mineral and metal resources",
                                               "embedded": {"value": 0.0383, "min": 0.0383, "max": 0.0383,
                                                            "warnings": ["Generic data used for impact calculation."]},
                                               "use": {"value": 0.0004, "min": 1.665e-05, "max": 0.006701}}},
                          "verbose": {"duration": {"value": 70080.0, "unit": "hours"},
                                      "avg_power": {"value": 300.0, "status": "ARCHETYPE", "unit": "W", "min": 60.0,
                                                    "max": 1200.0},
                                      "usage_location": {"value": "EEE", "status": "DEFAULT",
                                                         "unit": "CodSP3 - NCS Country Codes - NATO"},
                                      "use_time_ratio": {"value": 0.3, "status": "ARCHETYPE", "unit": "/1", "min": 0.3,
                                                         "max": 0.3},
                                      "hours_life_time": {"value": 70080.0, "status": "ARCHETYPE", "unit": "hours",
                                                          "min": 70080.0, "max": 70080.0},
                                      "adpe_factor": {"value": 6.42e-08, "status": "DEFAULT", "unit": "kg Sbeq/kWh",
                                                          "source": "ADEME Base IMPACTS ®", "min": 1.32e-08,
                                                          "max": 2.656e-07},
                                      "type": {"value": "perso", "status": "ARCHETYPE"},
                                      "units": {"value": 1, "status": "ARCHETYPE", "min": 1, "max": 1}}}


@pytest.mark.asyncio
async def test_tv_archetype_perso_duration():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/television?verbose=true&criteria=gwp&archetype=tv-perso&duration=1')

    assert res.status_code == 200
    assert res.json() == {"impacts": {"gwp": {"unit": "kgCO2eq", "description": "Total climate change",
                                              "embedded": {"value": 0.005137, "min": 0.005137, "max": 0.005137,
                                                           "warnings": ["Generic data used for impact calculation."]},
                                              "use": {"value": 0.03, "min": 0.000414, "max": 0.324}}},
                          "verbose": {"duration": {"value": 1.0, "unit": "hours"
                                                   },
                                      "avg_power": {"value": 300.0, "status": "ARCHETYPE", "unit": "W", "min": 60.0,
                                                    "max": 1200.0},
                                      "usage_location": {"value": "EEE", "status": "DEFAULT",
                                                         "unit": "CodSP3 - NCS Country Codes - NATO"},
                                      "use_time_ratio": {"value": 0.3, "status": "ARCHETYPE", "unit": "/1", "min": 0.3,
                                                         "max": 0.3},
                                      "hours_life_time": {"value": 70080.0, "status": "ARCHETYPE", "unit": "hours",
                                                          "min": 70080.0, "max": 70080.0},
                                      "gwp_factor": {"value": 0.38, "status": "DEFAULT", "unit": "kg CO2eq/kWh",
                                                     "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \nAverage of 27 european countries",
                                                     "min": 0.023, "max": 0.9},
                                      "type": {"value": "perso", "status": "ARCHETYPE"},
                                      "units": {"value": 1, "status": "ARCHETYPE", "min": 1, "max": 1}}}
