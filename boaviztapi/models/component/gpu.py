import math
import os

import pandas as pd

from boaviztapi import config, data_dir
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component.component import Component
from boaviztapi.models.impact import ImpactFactor
from boaviztapi.data.archetype import (
    get_arch_component,
    get_arch_value,
    get_component_archetype,
)
from boaviztapi.models.usage import ModelUsage
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_gpu_name

_gpu_specs = pd.read_csv(os.path.join(data_dir, "crowdsourcing/gpu_specs.csv"))
_default_gpu_archetype = get_component_archetype(config.default_gpu, "gpu")


def attributes_from_gpu_name(gpu_name: str):
    return fuzzymatch_attr_from_gpu_name(gpu_name, _gpu_specs)


_KERF = 0.2  # in mm
_WAFER_DIAMETER = 300  # in mm
_WAFER_SURFACE = math.pi * math.pow(_WAFER_DIAMETER / 2, 2)

# Factor to determine the area of vram die based on vram capacity, based on average of studied GPUs
VRAM_DIE_SURFACE_PER_GB = 15.5  # in mm2

# Idle power as a share of TDP, in line with the idle/max ranges of the Cloud
# Carbon Footprint GPU methodology (e.g. T4 8/71 W, A100 46/407 W)
IDLE_POWER_RATIO = 0.1


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


def gpu_usage_archetype(archetype) -> dict:
    """Usage archetype of a GPU: its host's, with the GPU's own default load.

    GPUs run at a different load than the CPU of their host: 60-70% for AI
    workloads at cloud providers (https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect).
    """
    usage = dict(get_arch_component(archetype, "USAGE") or {})
    default_usage = _default_gpu_archetype.get("USAGE", {})
    if "time_workload" in default_usage:
        usage["time_workload"] = default_usage["time_workload"]
    return usage


class ComponentGPU(Component):
    NAME = "GPU"
    _default_archetype = _default_gpu_archetype
    name_completion = False

    def __init__(
        self, archetype=get_component_archetype(config.default_gpu, "gpu"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)

        self.name = Boattribute(
            default=get_arch_value(archetype, "name", "default"),
            min=get_arch_value(archetype, "name", "min"),
            max=get_arch_value(archetype, "name", "max"),
        )

        self.manufacturer = Boattribute(
            complete_function=self._complete_from_name,
            default=get_arch_value(archetype, "manufacturer", "default"),
            min=get_arch_value(archetype, "manufacturer", "min"),
            max=get_arch_value(archetype, "manufacturer", "max"),
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
            complete_function=self._complete_from_name,
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

        self.tdp = Boattribute(
            complete_function=self._complete_tdp,
            unit="W",
            default=get_arch_value(archetype, "tdp", "default"),
            min=get_arch_value(archetype, "tdp", "min"),
            max=get_arch_value(archetype, "tdp", "max"),
        )

        # Cards such as the Tesla M60 carry two GPUs and providers count GPUs,
        # so one unit is then a share of the card
        self.gpus_per_card = Boattribute(
            complete_function=self._complete_gpus_per_card,
            default=get_arch_value(archetype, "gpus_per_card", "default", default=1),
            min=get_arch_value(archetype, "gpus_per_card", "min"),
            max=get_arch_value(archetype, "gpus_per_card", "max"),
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

    @property
    def usage(self) -> ModelUsage:
        if self._usage is None:
            self._usage = ModelUsage(archetype=gpu_usage_archetype(self.archetype))
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsage) -> None:
        self._usage = value

    def _complete_from_name(self):
        if self.name.has_value() and not self.name_completion:
            self.name_completion = True
            gpu_attributes = attributes_from_gpu_name(self.name.value)
            (
                name,
                manufacturer,
                vram_dies,
                vram,
                die_surface,
                pwb_surface,
                distance_boat,
                distance_truck,
                distance_plane,
                mass_casing,
                mass_heatsink,
                mass,
                tdp,
                gpus_per_card,
                source,
            ) = (
                gpu_attributes
                if gpu_attributes is not None
                else (
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            )

            if name is not None:
                self.name.set_completed(name, source="fuzzy match")
            if manufacturer is not None and self.manufacturer.is_none():
                self.manufacturer.set_completed(
                    manufacturer,
                    source=f"Completed from name based on {source}.",
                )
            if vram is not None and self.vram.is_none():
                self.vram.set_completed(
                    int(vram),
                    source=f"Completed from name based on {source}.",
                )
            if vram_dies is not None and self.vram_dies.is_none():
                self.vram_dies.set_completed(
                    int(vram_dies),
                    source=f"Completed from name based on {source}.",
                )
            # die_surface already includes wafer losses — use directly
            if die_surface is not None and self.gpu_surface.is_none():
                self.gpu_surface.set_completed(
                    die_surface,
                    source=f"Completed from name based on {source}.",
                )
            if pwb_surface is not None and self.pwb_surface.is_none():
                self.pwb_surface.set_completed(
                    pwb_surface,
                    source=f"Completed from name based on {source}.",
                )
            if distance_boat is not None and self.transport_boat.is_none():
                self.transport_boat.set_completed(
                    distance_boat,
                    source=f"Completed from name based on {source}.",
                )
            if distance_truck is not None and self.transport_truck.is_none():
                self.transport_truck.set_completed(
                    distance_truck,
                    source=f"Completed from name based on {source}.",
                )
            if distance_plane is not None and self.transport_plane.is_none():
                self.transport_plane.set_completed(
                    distance_plane,
                    source=f"Completed from name based on {source}.",
                )
            if mass_casing is not None and self.casing_weight.is_none():
                self.casing_weight.set_completed(
                    mass_casing,
                    source=f"Completed from name based on {source}.",
                )
            if mass_heatsink is not None and self.heatsink_weight.is_none():
                self.heatsink_weight.set_completed(
                    mass_heatsink,
                    source=f"Completed from name based on {source}.",
                )
            if mass is not None and self.weight.is_none():
                self.weight.set_completed(
                    mass,
                    source=f"Completed from name based on {source}.",
                )
            if tdp is not None and self.tdp.is_none():
                self.tdp.set_completed(
                    tdp,
                    source=f"Completed from name based on {source}.",
                    min=tdp,
                    max=tdp,
                )
            if gpus_per_card is not None and self.gpus_per_card.is_none():
                self.gpus_per_card.set_completed(
                    int(gpus_per_card),
                    source=f"Completed from name based on {source}.",
                )

    def _complete_weight(self):
        self._complete_from_name()
        if self.weight.is_set():
            return
        self.weight.set_archetype(
            get_arch_value(self._default_archetype, "weight", "default")
        )

    def _complete_heatsink_weight(self):
        self._complete_from_name()
        if self.heatsink_weight.is_set():
            return
        self.heatsink_weight.set_archetype(
            get_arch_value(self._default_archetype, "heatsink_weight", "default")
        )

    def _complete_pwb_surface(self):
        self._complete_from_name()
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
        self._complete_from_name()
        if self.casing_weight.is_set():
            return
        self.casing_weight.set_archetype(
            get_arch_value(self._default_archetype, "casing_weight", "default")
        )

    def _complete_gpu_surface(self):
        self._complete_from_name()
        if self.gpu_surface.is_set():
            return
        self.gpu_surface.set_archetype(
            _calculate_effective_area_on_circular_wafer(
                get_arch_value(self._default_archetype, "gpu_surface", "default")
            )
        )

    def _complete_vram_dies(self):
        self._complete_from_name()
        if self.vram_dies.is_set():
            return
        self.vram_dies.set_archetype(
            get_arch_value(self._default_archetype, "vram_dies", "default")
        )

    def _complete_tdp(self):
        self._complete_from_name()
        if self.tdp.is_set():
            return
        self.tdp.set_archetype(
            get_arch_value(self._default_archetype, "tdp", "default")
        )
        # The default TDP is a guess, so it keeps the range of the default GPU
        self.tdp.min = get_arch_value(self._default_archetype, "tdp", "min")
        self.tdp.max = get_arch_value(self._default_archetype, "tdp", "max")

    def _complete_gpus_per_card(self):
        self._complete_from_name()
        if self.gpus_per_card.is_set():
            return
        self.gpus_per_card.set_archetype(
            get_arch_value(
                self._default_archetype, "gpus_per_card", "default", default=1
            )
        )

    def _power_at_load(self, tdp: float, load: float) -> float:
        """Power of one GPU (W) at a load (%), linear from idle to the TDP of its card."""
        tdp_per_gpu = tdp / self.gpus_per_card.value
        return tdp_per_gpu * (IDLE_POWER_RATIO + (1 - IDLE_POWER_RATIO) * load / 100)

    def _power_at_workload(self, tdp: float, workload) -> float:
        """Power of one GPU (W) at a load (%) or a list of (time, load) pairs."""
        if type(workload) in (float, int):
            return self._power_at_load(tdp, workload)
        # The model is linear, so a list of (time, load) pairs is the same as
        # running at their time-weighted average load.
        return sum(
            w.time_percentage / 100 * self._power_at_load(tdp, w.load_percentage)
            for w in workload
        )

    def model_power_consumption(self) -> ImpactFactor:
        """Power of one GPU (W) from its TDP and the GPU load, with both ranges."""
        tdp = self.tdp.value  # completes tdp, and its bounds, if needed
        workload = self.usage.time_workload
        return ImpactFactor(
            value=self._power_at_workload(tdp, workload.value),
            min=self._power_at_workload(self.tdp.min, workload.min),
            max=self._power_at_workload(self.tdp.max, workload.max),
        )

    def complete_avg_power(self):
        """Model avg_power (per GPU) from the TDP, unless it was given."""
        if self.usage.avg_power.is_set():
            return
        consumption = self.model_power_consumption()
        self.usage.avg_power.set_completed(
            value=consumption.value, min=consumption.min, max=consumption.max
        )

    def _complete_transport_boat(self):
        self._complete_from_name()
        if self.transport_boat.is_set():
            return
        self.transport_boat.set_archetype(
            get_arch_value(self._default_archetype, "transport_boat", "default")
        )

    def _complete_transport_truck(self):
        self._complete_from_name()
        if self.transport_truck.is_set():
            return
        self.transport_truck.set_archetype(
            get_arch_value(self._default_archetype, "transport_truck", "default")
        )

    def _complete_transport_plane(self):
        self._complete_from_name()
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
