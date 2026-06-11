import pytest

from boaviztapi import config
from boaviztapi.compute.impacts_computation import gpu_impact_embedded
from boaviztapi.models.component import ComponentCPU, ComponentRAM
from boaviztapi.models.component.gpu import ComponentGPU, VRAM_DIE_SURFACE_PER_GB
from boaviztapi.models.device.server import DeviceServer
from boaviztapi.models.impact import IMPACT_CRITERIAS
from boaviztapi.models.usage import ModelUsage, ModelUsageServer
from boaviztapi.data.archetype import get_arch_value, get_component_archetype


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

    def test_all_fields_have_values_with_minimal_archetype(self):
        minimal_archetype = {
            "id": {"default": "test_gpu"},
            "name": {"default": "Test GPU"},
            "vram": {"default": 40},
        }
        gpu = ComponentGPU(archetype=minimal_archetype)

        # All fields should have values (from completion functions or defaults)
        assert gpu.weight.value is not None
        assert gpu.heatsink_weight.value is not None
        assert gpu.pwb_surface.value is not None
        assert gpu.casing_weight.value is not None
        assert gpu.gpu_surface.value is not None
        assert gpu.vram.value is not None
        assert gpu.vram_dies.value is not None
        assert gpu.vram_surface.value is not None
        assert gpu.transport_boat.value is not None
        assert gpu.transport_truck.value is not None
        assert gpu.transport_plane.value is not None

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
        archetype = get_component_archetype(config.default_gpu, "gpu")
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


class TestGPUEmbeddedImpact:
    def test_embedded_impact_scales_linearly_with_units(self):
        """Regression test for issue #527 (bug 1): embedded GPU impact must
        scale with ``gpu.units`` like every other component."""
        gpu_1 = ComponentGPU()
        gpu_1.units.set_input(1)

        gpu_8 = ComponentGPU()
        gpu_8.units.set_input(8)

        duration = gpu_1.usage.hours_life_time.value

        value_1, min_1, max_1, _ = gpu_impact_embedded("gwp", duration, gpu_1)
        value_8, min_8, max_8, _ = gpu_impact_embedded("gwp", duration, gpu_8)

        assert value_1 > 0
        assert value_8 == pytest.approx(value_1 * 8)
        assert min_8 == pytest.approx(min_1 * 8)
        assert max_8 == pytest.approx(max_1 * 8)


class TestServerGPUPower:
    @staticmethod
    def _build_server(gpu_avg_power=None, gpu_units=4):
        cpu = ComponentCPU()
        cpu.units.set_input(2)
        cpu.core_units.set_input(24)
        cpu.die_size_per_core.set_input(24.5)

        ram = ComponentRAM()
        ram.units.set_input(12)
        ram.capacity.set_input(32)
        ram.density.set_input(1.79)

        server = DeviceServer()
        server.cpu = cpu
        server.ram = [ram]
        server.usage = ModelUsageServer()

        if gpu_avg_power is not None:
            gpu = ComponentGPU()
            gpu.units.set_input(gpu_units)
            gpu.usage.avg_power.set_input(gpu_avg_power)
            server.gpu = gpu

        return server

    def test_gpu_power_added_to_server_power_consumption(self):
        """Regression test for issue #527 (bug 2): the modelled server power
        must include user-supplied GPU power."""
        baseline = self._build_server().model_power_consumption().value

        server_with_gpu = self._build_server(gpu_avg_power=400, gpu_units=4)
        with_gpu = server_with_gpu.model_power_consumption().value

        # 4 GPUs * 400 W of extra power, scaled by the "other consumption" overhead.
        overhead = 1 + server_with_gpu.usage.other_consumption_ratio.value
        assert with_gpu > baseline
        assert with_gpu == pytest.approx(baseline + 4 * 400 * overhead, rel=1e-6)

    def test_gpu_power_ignored_when_avg_power_not_provided(self):
        """Without a user-supplied avg_power the GPU has no power model, so the
        server power must be unchanged (GPU embedded impact still applies)."""
        baseline = self._build_server().model_power_consumption().value

        server_with_gpu = self._build_server()
        gpu = ComponentGPU()
        gpu.units.set_input(4)
        server_with_gpu.gpu = gpu

        assert server_with_gpu.model_power_consumption().value == pytest.approx(
            baseline
        )


class TestModelUsage:
    def test_all_impact_criterias_available_in_elec_factors(self):
        """Test that all factors in IMPACT_CRITERIAS are available in ModelUsage.elec_factors"""
        usage = ModelUsage(archetype={})

        # Get all keys in lowercase for comparison
        expected_factors = set(key.lower() for key in IMPACT_CRITERIAS.keys())
        actual_factors = set(key.lower() for key in usage.elec_factors.keys())

        # Check that all expected factors are present
        missing_factors = expected_factors - actual_factors
        assert not missing_factors, (
            f"Missing impact factors in ModelUsage.elec_factors: {missing_factors}"
        )

        # Check that all factors in elec_factors are valid (present in IMPACT_CRITERIAS)
        extra_factors = actual_factors - expected_factors
        assert not extra_factors, (
            f"Extra/invalid impact factors in ModelUsage.elec_factors: {extra_factors}"
        )

        # Verify exact match
        assert actual_factors == expected_factors, (
            f"Impact factors mismatch. Expected: {expected_factors}, Got: {actual_factors}"
        )
