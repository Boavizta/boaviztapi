from typing import Optional

from pydantic import Field

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.models.component import ComponentGPU
from boaviztapi.models.component.gpu import gpu_usage_archetype
from boaviztapi.data.archetype import get_component_archetype


class GPU(ComponentDTO):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    weight: Optional[float] = None
    heatsink_weight: Optional[float] = None
    pwb_surface: Optional[float] = None
    pwb_weight: Optional[float] = None
    casing_weight: Optional[float] = None
    gpu_surface: Optional[float] = None
    vram: Optional[int] = None
    vram_dies: Optional[int] = None
    vram_surface: Optional[float] = None
    tdp: Optional[float] = Field(default=None, ge=0)
    gpus_per_card: Optional[int] = Field(default=None, gt=0)
    transport_boat: Optional[float] = None
    transport_truck: Optional[float] = None
    transport_plane: Optional[float] = None


def mapper_gpu(
    gpu_dto: GPU, archetype=get_component_archetype(config.default_gpu, "gpu")
) -> ComponentGPU:
    gpu_component = ComponentGPU(archetype=archetype)

    gpu_component.usage = mapper_usage(
        gpu_dto.usage or Usage(), archetype=gpu_usage_archetype(archetype)
    )

    if gpu_dto.units is not None:
        gpu_component.units.set_input(gpu_dto.units)

    if gpu_dto.name is not None:
        gpu_component.name.set_input(gpu_dto.name)

    if gpu_dto.manufacturer is not None:
        gpu_component.manufacturer.set_input(gpu_dto.manufacturer)

    if gpu_dto.weight is not None:
        gpu_component.weight.set_input(gpu_dto.weight)

    if gpu_dto.heatsink_weight is not None:
        gpu_component.heatsink_weight.set_input(gpu_dto.heatsink_weight)

    if gpu_dto.pwb_surface is not None:
        gpu_component.pwb_surface.set_input(gpu_dto.pwb_surface)

    if gpu_dto.pwb_weight is not None:
        gpu_component.pwb_weight.set_input(gpu_dto.pwb_weight)

    if gpu_dto.casing_weight is not None:
        gpu_component.casing_weight.set_input(gpu_dto.casing_weight)

    if gpu_dto.gpu_surface is not None:
        gpu_component.gpu_surface.set_input(gpu_dto.gpu_surface)

    if gpu_dto.vram is not None:
        gpu_component.vram.set_input(gpu_dto.vram)

    if gpu_dto.vram_dies is not None:
        gpu_component.vram_dies.set_input(gpu_dto.vram_dies)

    if gpu_dto.vram_surface is not None:
        gpu_component.vram_surface.set_input(gpu_dto.vram_surface)

    if gpu_dto.tdp is not None:
        gpu_component.tdp.set_input(gpu_dto.tdp)

    if gpu_dto.gpus_per_card is not None:
        gpu_component.gpus_per_card.set_input(gpu_dto.gpus_per_card)

    if gpu_dto.transport_boat is not None:
        gpu_component.transport_boat.set_input(gpu_dto.transport_boat)

    if gpu_dto.transport_truck is not None:
        gpu_component.transport_truck.set_input(gpu_dto.transport_truck)

    if gpu_dto.transport_plane is not None:
        gpu_component.transport_plane.set_input(gpu_dto.transport_plane)

    return gpu_component
