from typing import List, Union, Optional
from fastapi import APIRouter, Query, Body

from boaviztapi import config
from boaviztapi.dto.device.user_terminal import Monitor, UsbStick, ExternalSSD, ExternalHDD
from boaviztapi.routers.openapi_doc.descriptions import all_archetype_user_terminals, all_peripheral_categories, \
    get_archetype_config_desc, peripheral_description
from boaviztapi.routers.openapi_doc.examples import end_user_terminal
from boaviztapi.routers.terminal_router import user_terminal_impact, get_all_archetype_name, get_archetype_config

peripheral_router = APIRouter(
    prefix='/v1/peripheral',
    tags=['peripheral']
)


@peripheral_router.get('/all',
                       description=all_peripheral_categories)
async def peripheral_get_all_categories():
    return {
        "monitor": "v1/peripheral/monitor",
        "usb_stick": "v1/peripheral/usb_stick",
        "external_ssd": "v1/peripheral/external_ssd",
        "external_hdd": "v1/peripheral/external_hdd"
    }


@peripheral_router.get('/monitor/archetypes',
                       description=all_archetype_user_terminals)
async def monitor_get_all_archetype_name():
    return get_all_archetype_name('monitor')


@peripheral_router.get('/monitor/archetype_config',
                       description=get_archetype_config_desc)
async def monitor_get_archetype_config(archetype: str = Query(example=config["default_monitor"])):
    return get_archetype_config(archetype)


@peripheral_router.post('/monitor', description=peripheral_description)
async def monitor_impact(monitor: Monitor = Body(None, example=end_user_terminal),
                         verbose: bool = True,
                         duration: Optional[float] = config["default_duration"],
                         archetype: str = config["default_monitor"],
                         criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=monitor,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/monitor', description=peripheral_description)
async def monitor_impact(archetype: str = config["default_monitor"],
                         verbose: bool = True,
                         duration: Optional[float] = config["default_duration"],
                         criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Monitor(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/usb_stick/archetypes',
                       description=all_archetype_user_terminals)
async def usb_stick_get_all_archetype_name():
    return get_all_archetype_name('usb_stick')


@peripheral_router.get('/usb_stick/archetype_config',
                       description=get_archetype_config_desc)
async def usb_stick_get_archetype_config(archetype: str = Query(example=config["default_usb_stick"])):
    return get_archetype_config(archetype)


@peripheral_router.post('/usb_stick', description=peripheral_description)
async def usb_stick_impact(usb_stick: UsbStick = Body(None, example=end_user_terminal),
                           verbose: bool = True,
                           duration: Optional[float] = config["default_duration"],
                           archetype: str = config["default_usb_stick"],
                           criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=usb_stick,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/usb_stick', description=peripheral_description)
async def usb_stick_impact(archetype: str = config["default_usb_stick"],
                           verbose: bool = True,
                           duration: Optional[float] = config["default_duration"],
                           criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=UsbStick(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/external_ssd/archetypes',
                       description=all_archetype_user_terminals)
async def external_ssd_get_all_archetype_name():
    return get_all_archetype_name('external_ssd')


@peripheral_router.get('/external_ssd/archetype_config',
                       description=get_archetype_config_desc)
async def external_ssd_get_archetype_config(archetype: str = Query(example=config["default_external_ssd"])):
    return get_archetype_config(archetype)


@peripheral_router.post('/external_ssd', description=peripheral_description)
async def external_ssd_impact(external_ssd: ExternalSSD = Body(None, example=end_user_terminal),
                              verbose: bool = True,
                              duration: Optional[float] = config["default_duration"],
                              archetype: str = config["default_external_ssd"],
                              criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=external_ssd,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/external_ssd', description=peripheral_description)
async def external_ssd_impact(archetype: str = config["default_external_ssd"],
                              verbose: bool = True,
                              duration: Optional[float] = config["default_duration"],
                              criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=ExternalSSD(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/external_hdd/archetypes',
                       description=all_archetype_user_terminals)
async def external_hdd_get_all_archetype_name():
    return get_all_archetype_name('external_hdd')


@peripheral_router.get('/external_hdd/archetype_config',
                       description=get_archetype_config_desc)
async def external_hdd_get_archetype_config(archetype: str = Query(example=config["default_external_hdd"])):
    return get_archetype_config(archetype)


@peripheral_router.post('/external_hdd', description=peripheral_description)
async def external_hdd_impact(external_hdd: ExternalHDD = Body(None, example=end_user_terminal),
                              verbose: bool = True,
                              duration: Optional[float] = config["default_duration"],
                              archetype: str = config["default_external_hdd"],
                              criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=external_hdd,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@peripheral_router.get('/external_hdd', description=peripheral_description)
async def external_hdd_impact(archetype: str = config["default_external_hdd"],
                              verbose: bool = True,
                              duration: Optional[float] = config["default_duration"],
                              criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=ExternalHDD(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)
