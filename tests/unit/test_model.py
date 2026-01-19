from boaviztapi import config
from boaviztapi.model.component.gpu import ComponentGPU, VRAM_DIE_SURFACE_PER_GB
from boaviztapi.service.archetype import get_arch_value, get_component_archetype


class TestComponentGPU:
    def test_values_from_default_archetype(self):
        gpu = ComponentGPU()

        # Populated from default archetype
        assert gpu.weight.has_value()
        assert gpu.heatsink_weight.has_value()
        assert gpu.pwb_surface.has_value()
        assert gpu.casing_weight.has_value()
        assert gpu.gpu_surface.has_value()
        assert gpu.vram.has_value()
        assert gpu.vram_dies.has_value()
        assert gpu.transport_boat.has_value()
        assert gpu.transport_truck.has_value()
        assert gpu.transport_plane.has_value()

        # Not populated from default archetype
        assert not gpu.pwb_weight.has_value()
        assert not gpu.vram_surface.has_value()

    def test_vram_surface_completion(self):
        gpu = ComponentGPU()

        # No default value
        assert not gpu.vram_surface.has_value()
        assert gpu.vram_surface.is_none()

        # Accessing triggers completion via wafer calculation
        value = gpu.vram_surface.value
        assert value is not None
        assert gpu.vram_surface.is_completed()

    def test_gpu_surface_computed_at_init(self):
        gpu = ComponentGPU()

        # Computed at initialization (no completion)
        assert gpu.gpu_surface.has_value()

        # Value is transformed from archetype via wafer calculation
        value = gpu.gpu_surface.value
        assert value is not None
        assert gpu.gpu_surface.is_archetype()

    def test_wafer_calculation_increases_surface_values(self):
        archetype = get_component_archetype(config["default_gpu"], "gpu")
        gpu = ComponentGPU()

        # GPU surface computed value should be larger than raw archetype value
        raw_gpu_surface = get_arch_value(archetype, "gpu_surface", "default")
        assert gpu.gpu_surface.value > raw_gpu_surface

        # VRAM surface computed value should be larger than raw die area
        # (raw vram_surface is empty, so we compare to the die area calculation)
        raw_vram = get_arch_value(archetype, "vram", "default")
        raw_vram_dies = get_arch_value(archetype, "vram_dies", "default")
        raw_die_area = (raw_vram * VRAM_DIE_SURFACE_PER_GB) / raw_vram_dies
        assert gpu.vram_surface.value > raw_die_area
