from typing import List

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config
from boaviztapi.dto.device.user_terminal import UserTerminal, mapper_user_terminal, Laptop, Desktop, Smartphone, \
    Monitor, Television, Smartwatch, UsbStick, ExternalSSD, ExternalHDD
from boaviztapi.routers.openapi_doc.examples import end_user_terminal
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.archetype import get_user_terminal_archetype
from boaviztapi.service.bottom_up import bottom_up
from boaviztapi.service.verbose import verbose_device

user_terminal_router = APIRouter(
    prefix='/v1/user_terminal',
    tags=['user_terminal']
)

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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/tablet', description="")
async def tablet_impact(tablet: Desktop = Body(None, example=end_user_terminal),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/box', description="")
async def box_impact(box: Smartwatch = Body(None, example=end_user_terminal),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
                         verbose=verbose,
                         allocation=allocation,
                         criteria=criteria,
                         archetype=archetype)

@user_terminal_router.post('/box', description="")
async def box_impact(box: Smartwatch = Body(None, example=end_user_terminal),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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

    return await user_terminal_impact(user_terminal_dto=Laptop(),
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