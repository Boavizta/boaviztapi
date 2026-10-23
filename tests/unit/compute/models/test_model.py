import pytest

from boaviztapi import config
from boaviztapi.compute.impacts_computation import gpu_impact_embedded
from boaviztapi.models.component import ComponentCPU, ComponentRAM
from boaviztapi.models.component.gpu import ComponentGPU, VRAM_DIE_SURFACE_PER_GB
from boaviztapi.models.device.server import DeviceServer
from boaviztapi.models.impact import IMPACT_CRITERIAS
from boaviztapi.models.usage import ModelUsage, ModelUsageServer
from boaviztapi.data.archetype import get_arch_value, get_component_archetype
from boaviztapi.dto.usage.usage import WorkloadTime


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

    def test_archetype_name_completes_from_gpu_specs(self):
        # Mirrors a server.csv GPU archetype: only units, name and vram are set
        archetype = {
            "units": {"default": 8},
            "name": {"default": "NVIDIA A100 SXM4 40GB"},
            "vram": {"default": 40},
        }
        gpu = ComponentGPU(archetype=archetype)

        # Reading the name used to recurse forever
        assert gpu.name.value == "NVIDIA A100 SXM4 40GB"
        assert gpu.gpu_surface.value == pytest.approx(1798.0)
        assert gpu.gpu_surface.is_completed()
        assert gpu.pwb_surface.value == pytest.approx(105.0)
        assert gpu.vram_dies.value == 6
        assert gpu.weight.value == pytest.approx(1.56)

    def test_input_name_completes_from_gpu_specs(self):
        gpu = ComponentGPU()
        gpu.name.set_input("NVIDIA L4")

        assert gpu.gpu_surface.value == pytest.approx(390.96)
        assert gpu.pwb_surface.value == pytest.approx(93.13)
        assert gpu.vram.value == 24
        assert gpu.manufacturer.value == "NVIDIA"

    def test_input_values_win_over_gpu_specs(self):
        gpu = ComponentGPU()
        gpu.name.set_input("NVIDIA L4")
        gpu.gpu_surface.set_input(1000)
        gpu.vram.set_input(48)

        assert gpu.gpu_surface.value == 1000
        assert gpu.vram.value == 48
        # Fields that were not input still come from gpu_specs
        assert gpu.pwb_surface.value == pytest.approx(93.13)

    def test_unknown_name_falls_back_to_default_archetype(self):
        default = ComponentGPU()
        gpu = ComponentGPU(
            archetype={"units": {"default": 1}, "name": {"default": "Unknown GPU"}}
        )

        assert gpu.gpu_surface.value == default.gpu_surface.value
        assert gpu.gpu_surface.is_archetype()


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

        # 4 GPUs * 400 W, added outside the "other consumption" overhead.
        assert with_gpu == pytest.approx(baseline + 4 * 400, rel=1e-6)

    def test_gpu_power_modelled_when_avg_power_not_provided(self):
        """Without a user-supplied avg_power, the GPU power is modelled from
        its TDP: 10% of it at idle, linear up to the TDP at full load."""
        baseline = self._build_server().model_power_consumption().value

        server_with_gpu = self._build_server()
        gpu = ComponentGPU()
        gpu.units.set_input(4)
        gpu.tdp.set_input(700)
        server_with_gpu.gpu = gpu

        # Default GPU load is 65%: 700 * (0.1 + 0.9 * 0.65) = 479.5 W per GPU
        power = server_with_gpu.model_power_consumption()
        assert gpu.usage.time_workload.value == 65
        assert gpu.usage.avg_power.value == pytest.approx(479.5)
        assert power.value == pytest.approx(baseline + 4 * 479.5)

    def test_gpu_power_bounds_follow_load_range(self):
        gpu = ComponentGPU()
        gpu.tdp.set_input(700)
        gpu.usage.time_workload.set_input(0)
        assert gpu.model_power_consumption().value == pytest.approx(70)
        gpu.usage.time_workload.set_input(100)
        assert gpu.model_power_consumption().value == pytest.approx(700)

    def test_gpu_power_from_multiple_workloads(self):
        gpu = ComponentGPU()
        gpu.tdp.set_input(700)
        gpu.usage.time_workload.set_input(
            [
                WorkloadTime(time_percentage=50, load_percentage=0),
                WorkloadTime(time_percentage=50, load_percentage=100),
            ]
        )
        # Same as a constant 50% load, since the model is linear
        assert gpu.model_power_consumption().value == pytest.approx(385)

    def test_gpu_tdp_completed_from_name(self):
        gpu = ComponentGPU()
        gpu.name.set_input("NVIDIA L4")
        assert gpu.tdp.value == 72
        assert gpu.gpus_per_card.value == 1

    def test_dual_gpu_card_power_is_per_gpu(self):
        """tdp is for the card; one unit of a two-GPU card gets half of it."""
        gpu = ComponentGPU()
        gpu.tdp.set_input(300)
        gpu.gpus_per_card.set_input(2)
        gpu.usage.time_workload.set_input(100)
        assert gpu.model_power_consumption().value == pytest.approx(150)

    def test_dual_gpu_card_embedded_is_per_gpu(self):
        def embedded(gpus_per_card):
            gpu = ComponentGPU()
            gpu.units.set_input(4)
            gpu.gpus_per_card.set_input(gpus_per_card)
            return gpu_impact_embedded("gwp", 1, gpu)[0]

        # 4 GPUs on two-GPU cards are 2 cards
        assert embedded(2) == pytest.approx(embedded(1) / 2)


class TestServerRAMPower:
    @staticmethod
    def _build_ram(units, capacity):
        ram = ComponentRAM()
        ram.units.set_input(units)
        ram.capacity.set_input(capacity)
        return ram

    def test_each_ram_bank_gets_its_own_power(self):
        """Each RAM entry of a server must report its own power, not the
        running total of the RAM entries before it."""
        server = DeviceServer()
        server.ram = [self._build_ram(4, 32), self._build_ram(2, 64)]
        server.usage = ModelUsageServer()

        server.model_power_consumption()

        for ram in server.ram:
            expected = self._build_ram(ram.units.value, ram.capacity.value)
            expected_power = expected.model_power_consumption()
            assert ram.usage.avg_power.value == pytest.approx(expected_power.value)
            assert ram.usage.avg_power.min == pytest.approx(expected_power.min)
            assert ram.usage.avg_power.max == pytest.approx(expected_power.max)


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

    @pytest.mark.parametrize(
        "criterion, location, expected",
        [
            ("gwppf", "FRA", (0.0813225, 0.0813225, 0.0813225)),
            # None uses config.default_location, which is EEE.
            ("gwppf", None, (0.509427, 0.00880732, 2.12572)),
        ],
    )
    def test_gwp_subcriteria_elec_factors_resolve(self, criterion, location, expected):
        """gwppf reads the gwpf electricity factor"""
        usage = ModelUsage(archetype={})
        if location:
            usage.usage_location.set_input(location)

        factor = usage.elec_factors[criterion]
        assert (factor.value, factor.min, factor.max) == pytest.approx(expected)
