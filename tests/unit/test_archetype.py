import os

import pytest

from boaviztapi.dto.device import Server
from boaviztapi.service.archetype import get_archetype
from tests.unit import data_dir

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_get_server_archetype_none():
    assert not get_archetype("nothing", csv_path=os.path.join(data_dir, "../data/devices/server/server.csv"))


@pytest.mark.asyncio
async def test_get_server_archetype_dellr740(dell_r740_dto):
    assert Server.parse_obj(get_archetype("dellR740", csv_path=os.path.join(data_dir, "../data/devices/server/server.csv"))) == dell_r740_dto