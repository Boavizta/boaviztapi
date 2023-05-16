import os
from typing import List
from unicodedata import category

import pandas as pd
from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device.user_terminal import UserTerminal, mapper_user_terminal, Laptop, Desktop, Smartphone, \
    Monitor, Television, UsbStick, ExternalSSD, ExternalHDD, Tablet, Box
from boaviztapi.routers.openapi_doc.descriptions import all_archetype_user_terminals, all_user_terminal_categories, all_user_terminal_subcategories, all_default_usage_values
from boaviztapi.routers.openapi_doc.examples import end_user_terminal
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.archetype import get_user_terminal_archetype, get_device_archetype_lst_with_type
from boaviztapi.service.bottom_up import bottom_up
from boaviztapi.service.verbose import verbose_device

user_terminal_router = APIRouter(
    prefix='/v1/user_terminal',
    tags=['user_terminal']
)

@user_terminal_router.get('/archetypes',
                   description=all_archetype_user_terminals)
async def server_get_all_archetype_name(name: str = Query("laptop")):
    result = get_device_archetype_lst_with_type(os.path.join(data_dir, 'archetypes/user_terminal.csv'), name.lower())
    if not result:
        return None
    return result

@user_terminal_router.get('/all_categories',
                   description=all_user_terminal_categories)
async def user_terminal_get_all_categories():
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/user_terminal.csv'))
    return df['device_type'].unique().tolist()

@user_terminal_router.get('/all_subcategories',
                   description=all_user_terminal_subcategories)
async def user_terminal_get_all_subcategories(category: str = Query(None, example="laptop")):
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/user_terminal.csv'))
    df2 =  df[df['device_type'] == category]
    if (df2.empty):
        raise HTTPException(status_code=404, detail=f"No data for this type of device ({category})")
    if (pd.isnull(df2['type']).all()):
        return [ "default" ]
    return df2['type'].unique().tolist()

@user_terminal_router.get('/all_default_usage_values',
                   description=all_default_usage_values)
async def user_terminal_get_default_usage_values(category: str = Query(None, example="laptop"),subcategory: str = Query(None, example="pro")):
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/user_terminal.csv'))
    if (category == None) | (subcategory == None):
        raise HTTPException(status_code=404, detail=f"Please specify category and subcategory.")
    df2 =  df[(df['device_type'] == category) & (df['type'] == subcategory)]
    if (df2.empty):
        raise HTTPException(status_code=404, detail=f"No data for this type of device ({category}) and subcategory ({subcategory})")
    result = {
        "hours_electrical_consumption": {
            "min":df2['USAGE.hours_electrical_consumption'].values[0].split(";")[1],
            "max":df2['USAGE.hours_electrical_consumption'].values[0].split(";")[2],
            "default":df2['USAGE.hours_electrical_consumption'].values[0].split(";")[0],
        },
        "use_time": str(df2['USAGE.use_time'].values[0]),
        "years_life_time": str(df2['USAGE.years_life_time'].values[0])
    }
    return result

@user_terminal_router.post('/laptop', description="")
async def laptop_impact(laptop: Laptop = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_laptop"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=laptop,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/laptop', description="")
async def laptop_impact(archetype: str = config["default_laptop"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Laptop(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/desktop', description="")
async def desktop_impact(desktop: Desktop = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_desktop"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=desktop,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/desktop', description="")
async def desktop_impact(archetype: str = config["default_desktop"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Desktop(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/monitor', description="")
async def monitor_impact(monitor: Monitor = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_monitor"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=monitor,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/monitor', description="")
async def monitor_impact(archetype: str = config["default_monitor"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Monitor(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/smartphone', description="")
async def smartphone_impact(smartphone: Smartphone = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_smartphone"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=smartphone,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/smartphone', description="")
async def smartphone_impact(archetype: str = config["default_smartphone"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Smartphone(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/tablet', description="")
async def tablet_impact(tablet: Tablet = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_tablet"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=tablet,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/tablet', description="")
async def tablet_impact(archetype: str = config["default_tablet"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Tablet(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/television', description="")
async def television_impact(television: Television = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_tv"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=television,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/television', description="")
async def television_impact(archetype: str = config["default_tv"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Television(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/box', description="")
async def box_impact(box: Box = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_box"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=box,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/box', description="")
async def box_impact(archetype: str = config["default_box"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=Box(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/usb_stick', description="")
async def usb_stick_impact(usb_stick: UsbStick = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_usb_stick"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=usb_stick,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/usb_stick', description="")
async def usb_stick_impact(archetype: str = config["default_usb_stick"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=UsbStick(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/external_ssd', description="")
async def external_ssd_impact(external_ssd: ExternalSSD = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_external_ssd"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=external_ssd,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/external_ssd', description="")
async def external_ssd_impact(archetype: str = config["default_external_ssd"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=ExternalSSD(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/external_hdd', description="")
async def external_hdd_impact(external_hdd: ExternalHDD = Body(None, example=end_user_terminal),
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        archetype: str = config["default_external_hdd"],
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=external_hdd,
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.get('/external_hdd', description="")
async def external_hdd_impact(archetype: str = config["default_external_hdd"],
                        verbose: bool = True,
                        allocation: Allocation = Allocation.TOTAL,
                        criteria: List[str] = Query(config["default_criteria"])):

    return await user_terminal_impact(user_terminal_dto=ExternalHDD(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

async def user_terminal_impact(user_terminal_dto: UserTerminal,
                         archetype:str,
                         verbose: bool, allocation: Allocation,
                         criteria: List[str] = Query(config["default_criteria"])) -> dict:
    archetype_config = get_user_terminal_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    device = mapper_user_terminal(user_terminal_dto, archetype=archetype_config)

    impacts = bottom_up(model=device, allocation=allocation, selected_criteria=criteria)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device, allocation=allocation, selected_criteria=criteria)
        }

    return impacts