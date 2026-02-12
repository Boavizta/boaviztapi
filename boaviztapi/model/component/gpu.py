import math
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_arch_value, get_component_archetype

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


class ComponentGPU(Component):
    NAME = "GPU"
    _default_archetype = get_component_archetype(config.default_gpu, "gpu")

    def __init__(
        self, archetype=get_component_archetype(config.default_gpu, "gpu"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)

        self.name = Boattribute(
            default=get_arch_value(archetype, "name", "default"),
            min=get_arch_value(archetype, "name", "min"),
            max=get_arch_value(archetype, "name", "max"),
        )

        self.weight = Boattribute(
            complete_function=self._complete_weight,
            unit="kg",
            default=get_arch_value(archetype, "weight", "default"),
            min=get_arch_value(archetype, "weight", "min"),
            max=get_arch_value(archetype, "weight", "max"),
        )

        self.heatsink_weight = Boattribute(
            complete_function=self._complete_heatsink_weight,
            unit="kg",
            default=get_arch_value(archetype, "heatsink_weight", "default"),
            min=get_arch_value(archetype, "heatsink_weight", "min"),
            max=get_arch_value(archetype, "heatsink_weight", "max"),
        )

        self.pwb_surface = Boattribute(
            complete_function=self._complete_pwb_surface,
            unit="cm2",
            default=get_arch_value(archetype, "pwb_surface", "default"),
            min=get_arch_value(archetype, "pwb_surface", "min"),
            max=get_arch_value(archetype, "pwb_surface", "max"),
        )

        self.pwb_weight = Boattribute(
            complete_function=self._complete_pwb_weight,
            unit="kg",
            default=get_arch_value(archetype, "pwb_weight", "default"),
            min=get_arch_value(archetype, "pwb_weight", "min"),
            max=get_arch_value(archetype, "pwb_weight", "max"),
        )

        self.casing_weight = Boattribute(
            complete_function=self._complete_casing_weight,
            unit="kg",
            default=get_arch_value(archetype, "casing_weight", "default"),
            min=get_arch_value(archetype, "casing_weight", "min"),
            max=get_arch_value(archetype, "casing_weight", "max"),
        )

        self.gpu_surface = Boattribute(
            complete_function=self._complete_gpu_surface,
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

        self.vram = Boattribute(
            unit="gb",
            default=get_arch_value(archetype, "vram", "default"),
            min=get_arch_value(archetype, "vram", "min"),
            max=get_arch_value(archetype, "vram", "max"),
        )

        self.vram_dies = Boattribute(
            complete_function=self._complete_vram_dies,
            default=get_arch_value(archetype, "vram_dies", "default"),
            min=get_arch_value(archetype, "vram_dies", "min"),
            max=get_arch_value(archetype, "vram_dies", "max"),
        )

        self.vram_surface = Boattribute(
            complete_function=self._complete_vram_surface,
            unit="mm2",
            default=get_arch_value(archetype, "vram_surface", "default"),
            min=get_arch_value(archetype, "vram_surface", "min"),
            max=get_arch_value(archetype, "vram_surface", "max"),
        )

        self.transport_boat = Boattribute(
            complete_function=self._complete_transport_boat,
            unit="km",
            default=get_arch_value(archetype, "transport_boat", "default"),
            min=get_arch_value(archetype, "transport_boat", "min"),
            max=get_arch_value(archetype, "transport_boat", "max"),
        )

        self.transport_truck = Boattribute(
            complete_function=self._complete_transport_truck,
            unit="km",
            default=get_arch_value(archetype, "transport_truck", "default"),
            min=get_arch_value(archetype, "transport_truck", "min"),
            max=get_arch_value(archetype, "transport_truck", "max"),
        )

        self.transport_plane = Boattribute(
            complete_function=self._complete_transport_plane,
            unit="km",
            default=get_arch_value(archetype, "transport_plane", "default"),
            min=get_arch_value(archetype, "transport_plane", "min"),
            max=get_arch_value(archetype, "transport_plane", "max"),
        )

    def _complete_weight(self):
        if self.weight.is_set():
            return
        self.weight.set_archetype(
            get_arch_value(self._default_archetype, "weight", "default")
        )

    def _complete_heatsink_weight(self):
        if self.heatsink_weight.is_set():
            return
        self.heatsink_weight.set_archetype(
            get_arch_value(self._default_archetype, "heatsink_weight", "default")
        )

    def _complete_pwb_surface(self):
        if self.pwb_surface.is_set():
            return
        self.pwb_surface.set_archetype(
            get_arch_value(self._default_archetype, "pwb_surface", "default")
        )

    def _complete_pwb_weight(self):
        if self.pwb_weight.is_set():
            return
        self.pwb_weight.set_archetype(
            get_arch_value(self._default_archetype, "pwb_weight", "default")
        )

    def _complete_casing_weight(self):
        if self.casing_weight.is_set():
            return
        self.casing_weight.set_archetype(
            get_arch_value(self._default_archetype, "casing_weight", "default")
        )

    def _complete_gpu_surface(self):
        if self.gpu_surface.is_set():
            return
        self.gpu_surface.set_archetype(
            _calculate_effective_area_on_circular_wafer(
                get_arch_value(self._default_archetype, "gpu_surface", "default")
            )
        )

    def _complete_vram_dies(self):
        if self.vram_dies.is_set():
            return
        self.vram_dies.set_archetype(
            get_arch_value(self._default_archetype, "vram_dies", "default")
        )

    def _complete_transport_boat(self):
        if self.transport_boat.is_set():
            return
        self.transport_boat.set_archetype(
            get_arch_value(self._default_archetype, "transport_boat", "default")
        )

    def _complete_transport_truck(self):
        if self.transport_truck.is_set():
            return
        self.transport_truck.set_archetype(
            get_arch_value(self._default_archetype, "transport_truck", "default")
        )

    def _complete_transport_plane(self):
        if self.transport_plane.is_set():
            return
        self.transport_plane.set_archetype(
            get_arch_value(self._default_archetype, "transport_plane", "default")
        )

    def _complete_vram_surface(self):
        if self.vram_surface.is_set():
            return

        # If we have no vram or vram_dies, we have to set to zero
        if not self.vram.has_value() and not self.vram_dies.has_value():
            self.vram_surface.set_completed(0)
            return

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
