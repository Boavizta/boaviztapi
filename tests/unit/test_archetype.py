import os

import pytest

from boaviztapi.dto.device import Server
from boaviztapi.service.archetype import get_archetype
from tests.unit import data_dir

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_get_server_archetype_none():
    assert not get_archetype("nothing", csv_path=os.path.join(data_dir, "archetypes/server.csv"))


@pytest.mark.asyncio
async def test_get_server_archetype_dellr740():
    assert get_archetype("dellR740", csv_path=os.path.join(data_dir, "archetypes/server.csv")) == {'CASE': {'case_type': {'default': 'rack'}},
                                                                                                   'CPU': {'core_units': {'default': 24.0},
                                                                                                           'die_size_per_core': {'default': 0.245},
                                                                                                           'family': {},
                                                                                                           'manufacturer': {},
                                                                                                           'model_range': {},
                                                                                                           'name': {},
                                                                                                           'tdp': {},
                                                                                                           'units': {'default': 2.0}},
                                                                                                   'HDD': {'capacity': {}, 'units': {}},
                                                                                                   'POWER_SUPPLY': {'unit_weight': {'default': 2.99, 'max': 5.0, 'min': 1.0},
                                                                                                                    'units': {'default': 2.0, 'max': 2.0, 'min': 1.0}},
                                                                                                   'RAM': {'capacity': {'default': 32.0},
                                                                                                           'density': {'default': 1.79},
                                                                                                           'units': {'default': 12.0}},
                                                                                                   'SSD': {'capacity': {'default': 400.0},
                                                                                                           'density': {'default': 50.6},
                                                                                                           'units': {'default': 1.0}},
                                                                                                   'USAGE': {'other_consumption_ratio': {'default': 0.33},
                                                                                                             'time_workload': {'default': 50.0, 'max': 100.0, 'min': 0.0},
                                                                                                             'use_time': {'default': 8760.0, 'max': 87600.0, 'min': 1.0},
                                                                                                             'life_time': {'default': 26280.0,
                                                                                                                                 'max': 87600.0,
                                                                                                                                 'min': 8760.0}},
                                                                                                   'WARNINGS': {},
                                                                                                   'manufacturer': {'default': 'Dell'}}