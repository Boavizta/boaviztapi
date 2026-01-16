from typing import Optional

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.component import ComponentGPU
from boaviztapi.service.archetype import get_component_archetype


class GPU(ComponentDTO):
    weight: Optional[float] = None
    heatsink_weight: Optional[float] = None
    pwb_surface: Optional[float] = None
    pwb_weight: Optional[float] = None
    casing_weight: Optional[float] = None
    gpu_surface: Optional[float] = None
    vram: Optional[int] = None
    vram_dies: Optional[int] = None
    vram_surface: Optional[float] = None
    transport_boat: Optional[float] = None
    transport_truck: Optional[float] = None
    transport_plane: Optional[float] = None


def mapper_gpu(
    gpu_dto: GPU, archetype=get_component_archetype(config["default_gpu"], "gpu")
) -> ComponentGPU:
    gpu_component = ComponentGPU(archetype=archetype)

    gpu_component.usage = mapper_usage(
        gpu_dto.usage or Usage(), archetype=archetype.get("USAGE")
    )

    if gpu_dto.units is not None:
        gpu_component.units.set_input(gpu_dto.units)

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

    if gpu_dto.transport_boat is not None:
        gpu_component.transport_boat.set_input(gpu_dto.transport_boat)

    if gpu_dto.transport_truck is not None:
        gpu_component.transport_truck.set_input(gpu_dto.transport_truck)

    if gpu_dto.transport_plane is not None:
        gpu_component.transport_plane.set_input(gpu_dto.transport_plane)

    return gpu_component
