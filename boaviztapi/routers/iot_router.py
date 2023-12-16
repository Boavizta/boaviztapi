import os
from typing import Optional, List

import pandas as pd
from fastapi import APIRouter, Body, Query, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device.iot import IoT, mapper_iot_device
from boaviztapi.service.archetype import get_iot_device_archetype
from boaviztapi.service.impacts_computation import compute_impacts
from boaviztapi.service.verbose import verbose_device

iot = APIRouter(
    prefix='/v1/iot',
    tags=['iot']
)


@iot.get('/iot_device/archetypes',
         description="")
async def iot_device_get_all_archetype_name():
    df = pd.read_csv(os.path.join(data_dir, "archetypes/iot_device.csv"))
    return df['id'].tolist()


@iot.get('/iot_device/archetype_config',
         description="")
async def get_archetype_config(archetype: str = Query(example=config["default_iot_device"])):
    archetype_config = get_iot_device_archetype(archetype)
    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")
    return archetype_config


@iot.post('/iot_device', description="")
async def iot_device_impact(iot: IoT = Body(None, example=""),
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            archetype: str = config["default_iot_device"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await device_iot_impact(iot_dto=iot,
                                   verbose=verbose,
                                   duration=duration,
                                   criteria=criteria,
                                   archetype=archetype)


@iot.get('/iot_device', description="")
async def iot_device_impact(archetype: str = config["default_iot_device"],
                            verbose: bool = True,
                            duration: Optional[float] = config["default_duration"],
                            criteria: List[str] = Query(config["default_criteria"])):
    return await device_iot_impact(iot_dto=IoT(),
                                   verbose=verbose,
                                   duration=duration,
                                   criteria=criteria,
                                   archetype=archetype)


async def device_iot_impact(iot_dto: IoT,
                            archetype: str,
                            verbose: bool,
                            duration: Optional[float] = config["default_duration"],
                            criteria: List[str] = Query(config["default_criteria"])) -> dict:
    archetype_config = get_iot_device_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    device = mapper_iot_device(iot_dto, archetype=archetype_config)

    if duration is None:
        duration = device.usage.hours_life_time.value

    impacts = compute_impacts(model=device, selected_criteria=criteria, duration=duration)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device, selected_criteria=criteria, duration=duration)
        }

    return {"impacts": impacts}
