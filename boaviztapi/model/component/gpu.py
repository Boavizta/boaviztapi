import math
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_arch_value, get_component_archetype
from typing import Union

_KERF = 0.2  # in mm
_WAFER_DIAMETER = 300  # in mm
_WAFER_SURFACE = math.pi * math.pow(_WAFER_DIAMETER / 2, 2)

# Factor to determine the area of vram die based on vram capacity, based on average of studied GPUs
VRAM_DIE_SURFACE_PER_GB = 15.5  # in mm2


def _calculate_effective_area_on_circular_wafer(die_area: float | None) -> float | None:
    if die_area is None:
        return None

    # Add kerf (space between dies) to width and calculate actual area of the wafer used for the die
    die_width = math.sqrt(die_area) + _KERF
    actual_die_area = math.pow(die_width, 2)

    # Number of dies per wafer, see following for explanation:
    # https://math.stackexchange.com/questions/3007527/how-many-squares-fit-in-a-circle
    n_dies_per_wafer = (_WAFER_SURFACE / actual_die_area) - (
        (math.pi * _WAFER_DIAMETER) / math.sqrt(2 * actual_die_area)
    )

    # Total surface of chips on the wafer
    total_die_area = n_dies_per_wafer * actual_die_area

    # Effective area of wafer used per die, sharing all wafer area across dies
    effective_die_area = actual_die_area * (_WAFER_SURFACE / total_die_area)

    # Calculate the ratio of manufactured dies that are usable (decreases as dies get larger)
    usable_ratio = math.exp(-math.sqrt((actual_die_area / 100) * 0.1))

    return effective_die_area / usable_ratio


def _get_archetype_value(
    archetype: Union[dict, bool], attribute: str, unit: str | None = None
) -> Boattribute:
    return Boattribute(
        unit=unit,
        default=get_arch_value(archetype, attribute, "default"),
        min=get_arch_value(archetype, attribute, "min"),
        max=get_arch_value(archetype, attribute, "max"),
    )


class ComponentGPU(Component):
    NAME = "GPU"

    def __init__(
        self, archetype=get_component_archetype(config["default_gpu"], "gpu"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)

        self.weight = _get_archetype_value(archetype, "weight", unit="kg")

        self.heatsink_weight = _get_archetype_value(
            archetype, "heatsink_weight", unit="kg"
        )

        self.pwb_surface = _get_archetype_value(archetype, "pwb_surface", unit="cm2")

        self.pwb_weight = _get_archetype_value(archetype, "pwb_weight", unit="kg")

        self.casing_weight = _get_archetype_value(archetype, "casing_weight", unit="kg")

        # Total effective GPU area including losses
        self.gpu_surface = Boattribute(
            unit="mm2",
            default=_calculate_effective_area_on_circular_wafer(
                get_arch_value(archetype, "gpu_surface", "default"),
            ),
            min=_calculate_effective_area_on_circular_wafer(
                get_arch_value(archetype, "gpu_surface", "min"),
            ),
            max=_calculate_effective_area_on_circular_wafer(
                get_arch_value(archetype, "gpu_surface", "max"),
            ),
        )

        self.vram = _get_archetype_value(archetype, "vram", unit="gb")

        self.vram_dies = _get_archetype_value(archetype, "vram_dies")

        self.vram_surface = Boattribute(
            complete_function=self._complete_vram_surface,
            unit="mm2",
            default=get_arch_value(archetype, "vram_surface", "default"),
            min=get_arch_value(archetype, "vram_surface", "min"),
            max=get_arch_value(archetype, "vram_surface", "max"),
        )

        self.transport_boat = _get_archetype_value(
            archetype, "transport_boat", unit="km"
        )

        self.transport_truck = _get_archetype_value(
            archetype, "transport_truck", unit="km"
        )

        self.transport_plane = _get_archetype_value(
            archetype, "transport_plane", unit="km"
        )

    def _complete_vram_surface(self):
        if self.vram_surface.is_set():
            # Ignore if explicitly set
            return

        # If we have no vram or vram_dies, we have to set to zero
        if not self.vram.is_set() and not self.vram_dies.is_set():
            self.vram_surface.set_completed(0)

        # Area per die using the model
        die_area = (self.vram.value * VRAM_DIE_SURFACE_PER_GB) / self.vram_dies.value
        die_area_min = (self.vram.min * VRAM_DIE_SURFACE_PER_GB) / self.vram_dies.min
        die_area_max = (self.vram.max * VRAM_DIE_SURFACE_PER_GB) / self.vram_dies.max

        # Total effective area including losses
        effective_area = _calculate_effective_area_on_circular_wafer(die_area=die_area)
        effective_area_min = _calculate_effective_area_on_circular_wafer(
            die_area=die_area_min
        )
        effective_area_max = _calculate_effective_area_on_circular_wafer(
            die_area=die_area_max
        )

        total_effective_area = effective_area * self.vram_dies.value
        total_effective_area_min = effective_area_min * self.vram_dies.min
        total_effective_area_max = effective_area_max * self.vram_dies.max

        self.vram_surface.set_completed(
            value=total_effective_area,
            min=total_effective_area_min,
            max=total_effective_area_max,
        )
