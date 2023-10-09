import os
from typing import List, Union, Optional

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device.user_terminal import UserTerminal, mapper_user_terminal, Laptop, Desktop, Smartphone, \
    Television, Tablet, Box
from boaviztapi.routers.openapi_doc.descriptions import all_archetype_user_terminals, all_terminal_categories, \
    get_archetype_config_desc, terminal_description
from boaviztapi.routers.openapi_doc.examples import end_user_terminal
from boaviztapi.service.archetype import get_user_terminal_archetype, get_device_archetype_lst_with_type
from boaviztapi.service.bottom_up import bottom_up
from boaviztapi.service.verbose import verbose_device

terminal_router = APIRouter(
    prefix='/v1/terminal',
    tags=['terminal']
)


@terminal_router.get('/all',
                     description=all_terminal_categories)
async def terminal_get_all_categories():
    return {
        "laptop": "v1/terminal/laptop",
        "desktop": "v1/terminal/desktop",
        "smartphone": "v1/terminal/smartphone",
        "television": "v1/terminal/television",
        "tablet": "v1/terminal/tablet",
        "box": "v1/terminal/box"
    }


@terminal_router.get('/laptop/archetypes',
                     description=all_archetype_user_terminals)
async def laptop_get_all_archetype_name():
    return get_all_archetype_name('laptop')


@terminal_router.get('/laptop/archetype_config',
                     description=get_archetype_config_desc)
async def laptop_get_archetype_config(archetype: str = Query(example=config["default_laptop"])):
    return get_archetype_config(archetype)


@terminal_router.post('/laptop', description=terminal_description)
async def laptop_impact(laptop: Laptop = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        duration: Optional[float] = config["default_duration"],
                        archetype: str = config["default_laptop"],
                        criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=laptop,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/laptop', description=terminal_description)
async def laptop_impact(archetype: str = config["default_laptop"],
                        verbose: bool = True,
                        duration: Optional[float] = config["default_duration"],
                        criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Laptop(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/desktop/archetypes',
                     description=all_archetype_user_terminals)
async def desktop_get_all_archetype_name():
    return get_all_archetype_name('desktop')


@terminal_router.get('/desktop/archetype_config',
                     description=get_archetype_config_desc)
async def desktop_get_archetype_config(archetype: str = Query(example=config["default_desktop"])):
    return get_archetype_config(archetype)


@terminal_router.post('/desktop', description=terminal_description)
async def desktop_impact(desktop: Desktop = Body(None, example=end_user_terminal),
                         verbose: bool = True,
                         duration: Optional[float] = config["default_duration"],
                         archetype: str = config["default_desktop"],
                         criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=desktop,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/desktop', description=terminal_description)
async def desktop_impact(archetype: str = config["default_desktop"],
                         verbose: bool = True,
                         duration: Optional[float] = config["default_duration"],
                         criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Desktop(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/smartphone/archetypes',
                     description=all_archetype_user_terminals)
async def smartphone_get_all_archetype_name():
    return get_all_archetype_name('smartphone')


@terminal_router.get('/smartphone/archetype_config',
                     description=get_archetype_config_desc)
async def smartphone_get_archetype_config(archetype: str = Query(example=config["default_smartphone"])):
    return get_archetype_config(archetype)


@terminal_router.post('/smartphone', description=terminal_description)
async def smartphone_impact(smartphone: Smartphone = Body(None, example=end_user_terminal),
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            archetype: str = config["default_smartphone"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=smartphone,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/smartphone', description=terminal_description)
async def smartphone_impact(archetype: str = config["default_smartphone"],
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Smartphone(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/tablet/archetypes',
                     description=all_archetype_user_terminals)
async def tablet_get_all_archetype_name():
    return get_all_archetype_name('tablet')


@terminal_router.get('/tablet/archetype_config',
                     description=get_archetype_config_desc)
async def tablet_get_archetype_config(archetype: str = Query(example=config["default_tablet"])):
    return get_archetype_config(archetype)


@terminal_router.post('/tablet', description=terminal_description)
async def tablet_impact(tablet: Tablet = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        duration: Optional[float] = config["default_duration"],
                        archetype: str = config["default_tablet"],
                        criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=tablet,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/tablet', description=terminal_description)
async def tablet_impact(archetype: str = config["default_tablet"],
                        verbose: bool = True,
                        duration: Optional[float] = config["default_duration"],
                        criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Tablet(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/television/archetypes',
                     description=all_archetype_user_terminals)
async def television_get_all_archetype_name():
    return get_all_archetype_name('television')


@terminal_router.get('/television/archetype_config',
                     description=get_archetype_config_desc)
async def television_get_archetype_config(archetype: str = Query(example=config["default_television"])):
    return get_archetype_config(archetype)


@terminal_router.post('/television', description=terminal_description)
async def television_impact(television: Television = Body(None, example=end_user_terminal),
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            archetype: str = config["default_television"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=television,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/television', description=terminal_description)
async def television_impact(archetype: str = config["default_television"],
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Television(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/box/archetypes',
                     description=all_archetype_user_terminals)
async def box_get_all_archetype_name():
    return get_all_archetype_name('box')


@terminal_router.get('/box/archetype_config',
                     description=get_archetype_config_desc)
async def box_get_archetype_config(archetype: str = Query(example=config["default_box"])):
    return get_archetype_config(archetype)


@terminal_router.post('/box', description=terminal_description)
async def box_impact(box: Box = Body(None, example=end_user_terminal),
                     verbose: bool = True,
                     duration: Optional[float] = config["default_duration"],
                     archetype: str = config["default_box"],
                     criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=box,
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


@terminal_router.get('/box', description=terminal_description)
async def box_impact(archetype: str = config["default_box"],
                     verbose: bool = True,
                     duration: Optional[float] = config["default_duration"],
                     criteria: List[str] = Query(config["default_criteria"])):
    return await user_terminal_impact(user_terminal_dto=Box(),
                                      verbose=verbose,
                                      duration=duration,
                                      criteria=criteria,
                                      archetype=archetype)


async def user_terminal_impact(user_terminal_dto: UserTerminal,
                               archetype: str,
                               verbose: bool,
                               duration: Optional[float] = config["default_duration"],
                               criteria: List[str] = Query(config["default_criteria"])) -> dict:
    archetype_config = get_user_terminal_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    device = mapper_user_terminal(user_terminal_dto, archetype=archetype_config)

    if duration is None:
        duration = device.usage.hours_life_time.value

    impacts = bottom_up(model=device, selected_criteria=criteria, duration=duration)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device, selected_criteria=criteria, duration=duration)
        }

    return {"impacts": impacts}


def get_all_archetype_name(name: str):
    result = get_device_archetype_lst_with_type(os.path.join(data_dir, 'archetypes/user_terminal.csv'), name.lower())
    if not result:
        return None
    return result


def get_archetype_config(archetype: str):
    result = get_user_terminal_archetype(archetype)
    if not result:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")
    return result
