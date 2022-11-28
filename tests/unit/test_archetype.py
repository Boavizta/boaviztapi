import os

import pytest

from boaviztapi.dto.device import Server
from boaviztapi.service.archetype import get_server_archetype, complete_with_archetype, get_archetype
from tests.unit import data_dir

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_get_server_archetype_none():
    assert not get_archetype("nothing", csv_path=os.path.join(data_dir, "devices/server/server.csv"))


@pytest.mark.asyncio
async def test_get_server_archetype_dellr740(dell_r740_dto):
    assert Server.parse_obj(get_archetype("dellR740", csv_path=os.path.join(data_dir, 'devices/server/server.csv'))) == dell_r740_dto


def test_complete_with_archetype_empty(dell_r740_dto, empty_server_dto):
    assert Server(**complete_with_archetype(empty_server_dto, dell_r740_dto)) == dell_r740_dto


def test_complete_with_archetype_incomplete(dell_r740_dto, incomplete_server_dto, completed_server_with_dellr740_dto):
    assert Server(**complete_with_archetype(incomplete_server_dto, dell_r740_dto)) == completed_server_with_dellr740_dto


def test_complete_with_archetype_partial_usage(incomplete_usage_dto, cloud_instance_1_completed_dto):
    assert complete_with_archetype(incomplete_usage_dto, cloud_instance_1_completed_dto) == cloud_instance_1_completed_dto
