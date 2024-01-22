from typing import Optional

from boaviztapi import config
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import mapper_usage, Usage
from boaviztapi.model.component.gpu import ComponentGPU
from boaviztapi.service.archetype import get_component_archetype, get_arch_value


class GPU(ComponentDTO):
    name: Optional[str] = None
    family: Optional[str] = None
    manufacturer: Optional[str] = None
    tdp: Optional[float] = None
    gpu_name: Optional[str] = None
    gpu_variant: Optional[str] = None
    gpu_architecture: Optional[str] = None
    gpu_die_size: Optional[float] = None
    gpu_process: Optional[float] = None
    vram_capacity: Optional[int] = None
    vram_density: Optional[float] = None
    pcb_size: Optional[float] = None
    pcb_dim_x: Optional[float] = None
    pcb_dim_y: Optional[float] = None
    pcie: Optional[str] = None


def mapper_gpu(gpu_dto: GPU, archetype=get_component_archetype(config["default_gpu"], "gpu")) -> ComponentGPU:
    gpu_component = ComponentGPU(archetype=archetype)
    gpu_component.usage = mapper_usage(gpu_dto.usage or Usage(), archetype=archetype.get("USAGE"))

    if gpu_dto.name is not None:
        gpu_component.name.set_input(gpu_dto.name)

    if gpu_dto.family is not None:
        gpu_component.family.set_input(gpu_dto.family)

    if gpu_dto.manufacturer is not None:
        gpu_component.manufacturer.set_input(gpu_dto.manufacturer)

    if gpu_dto.gpu_name is not None:
        gpu_component.gpu_name.set_input(gpu_dto.gpu_name)

    if gpu_dto.gpu_variant is not None:
        gpu_component.gpu_variant.set_input(gpu_dto.gpu_variant)

    if gpu_dto.gpu_architecture is not None:
        gpu_component.gpu_architecture.set_input(gpu_dto.gpu_architecture)

    if gpu_dto.gpu_die_size is not None:
        gpu_component.gpu_die_size.set_input(gpu_dto.gpu_die_size)

    if gpu_dto.gpu_process is not None:
        gpu_component.gpu_process.set_input(gpu_dto.gpu_process)

    if gpu_dto.vram_capacity is not None:
        gpu_component.vram_capacity.set_input(gpu_dto.vram_capacity)

    if gpu_dto.vram_density is not None:
        gpu_component.vram_density.set_input(gpu_dto.vram_density)

    if gpu_dto.pcb_size is not None:
        gpu_component.pcb_size.set_input(gpu_dto.pcb_size)
        gpu_component.pcb_size.set_input(gpu_dto.pcb_size)
    elif gpu_dto.pcb_dim_x is not None and gpu_dto.pcb_dim_y is not None:
        gpu_component.pcb_size.set_input(gpu_dto.pcb_dim_x * gpu_dto.pcb_dim_y)

    if gpu_dto.pcie is not None:
        gpu_component.pcie.set_input(gpu_dto.pcie)

    return gpu_component
