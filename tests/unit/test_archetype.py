import os

from boaviztapi.dto.server_dto import ServerDTO
from boaviztapi.service.archetype import get_server_archetype_lst, get_server_archetype, complete_with_archetype
from tests.unit import data_dir


def test_get_device_archetype_lst():
    assert get_server_archetype_lst(path=os.path.join(data_dir, 'devices/server')) == ['dellR740', 'incomplete']


def test_get_server_archetype_none():
    assert not get_server_archetype("nothing", path=os.path.join(data_dir, 'devices/server'))


def test_get_server_archetype_dellr740(dell_r740):
    assert get_server_archetype("dellR740", path=os.path.join(data_dir, 'devices/server')) == dell_r740


def test_complete_with_archetype_empty(dell_r740, empty_server):
    assert complete_with_archetype(empty_server, dell_r740) == dell_r740
