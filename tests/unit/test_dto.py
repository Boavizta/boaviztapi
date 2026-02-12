from boaviztapi.dto.component import CPU, GPU, RAM, Disk, PowerSupply
from boaviztapi.dto.component.gpu import mapper_gpu
from boaviztapi.dto.device.device import (
    Server,
    ModelServer,
    ConfigurationServer,
    mapper_server,
)
from boaviztapi.dto.usage import UsageServer
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import (
    ComponentCPU,
    ComponentGPU,
    ComponentRAM,
    ComponentSSD,
    ComponentPowerSupply,
    ComponentCase,
    ComponentMotherboard,
    ComponentAssembly,
)


class TestGPUMapping:
    def test_maps_all_fields(self):
        gpu_dto = GPU(
            units=2,
            name="NVIDIA A100",
            weight=1.5,
            heatsink_weight=0.3,
            pwb_surface=100.0,
            pwb_weight=0.2,
            casing_weight=0.5,
            gpu_surface=500.0,
            vram=24,
            vram_dies=6,
            vram_surface=200.0,
            transport_boat=1000.0,
            transport_truck=500.0,
            transport_plane=100.0,
        )

        component = mapper_gpu(gpu_dto)

        assert component.units.value == gpu_dto.units
        assert component.name.value == gpu_dto.name
        assert component.weight.value == gpu_dto.weight
        assert component.heatsink_weight.value == gpu_dto.heatsink_weight
        assert component.pwb_surface.value == gpu_dto.pwb_surface
        assert component.pwb_weight.value == gpu_dto.pwb_weight
        assert component.casing_weight.value == gpu_dto.casing_weight
        assert component.gpu_surface.value == gpu_dto.gpu_surface
        assert component.vram.value == gpu_dto.vram
        assert component.vram_dies.value == gpu_dto.vram_dies
        assert component.vram_surface.value == gpu_dto.vram_surface
        assert component.transport_boat.value == gpu_dto.transport_boat
        assert component.transport_truck.value == gpu_dto.transport_truck
        assert component.transport_plane.value == gpu_dto.transport_plane


class TestServerMapping:
    def test_maps_all_components(self):
        """Test that mapper_server maps all components from the DTO to the model."""
        server_dto = Server(
            model=ModelServer(type="rack"),
            configuration=ConfigurationServer(
                cpu=CPU(units=2, core_units=24, name="intel xeon gold 6134"),
                ram=[RAM(units=12, capacity=32)],
                disk=[Disk(units=1, type="ssd", capacity=400)],
                gpu=GPU(units=2, vram=40),
                power_supply=PowerSupply(unit_weight=2.99),
            ),
            usage=UsageServer(hours_life_time=35040),
        )

        server_model = mapper_server(server_dto)

        # CPU
        assert isinstance(server_model.cpu, ComponentCPU)
        assert server_model.cpu.units.value == 2
        assert server_model.cpu.core_units.value == 24
        assert server_model.cpu.name.value == "intel xeon gold 6134"

        # RAM
        assert len(server_model.ram) == 1
        assert isinstance(server_model.ram[0], ComponentRAM)
        assert server_model.ram[0].units.value == 12
        assert server_model.ram[0].capacity.value == 32

        # Disk
        assert len(server_model.disk) == 1
        assert isinstance(server_model.disk[0], ComponentSSD)
        assert server_model.disk[0].units.value == 1
        assert server_model.disk[0].capacity.value == 400

        # GPU
        assert isinstance(server_model.gpu, ComponentGPU)
        assert server_model.gpu.units.value == 2
        assert server_model.gpu.vram.value == 40

        # Power supply
        assert isinstance(server_model.power_supply, ComponentPowerSupply)
        assert server_model.power_supply.unit_weight.value == 2.99

        # Case type from model.type
        assert isinstance(server_model.case, ComponentCase)
        assert server_model.case.case_type.value == "rack"
        assert server_model.case.case_type.status == Status.INPUT

        # Archetype-provided components
        assert isinstance(server_model.motherboard, ComponentMotherboard)
        assert isinstance(server_model.assembly, ComponentAssembly)

        # Usage
        assert server_model.usage.hours_life_time.value == 35040

        # Components list includes all mapped components
        components = server_model.components
        component_types = [type(c) for c in components]
        assert ComponentAssembly in component_types
        assert ComponentCPU in component_types
        assert ComponentGPU in component_types
        assert ComponentRAM in component_types
        assert ComponentSSD in component_types
        assert ComponentPowerSupply in component_types
        assert ComponentCase in component_types
        assert ComponentMotherboard in component_types

    def test_gpu_usage_is_propagated(self):
        """Test that device-level usage is propagated to the GPU component."""
        server_dto = Server(
            configuration=ConfigurationServer(
                gpu=GPU(units=2, vram=40),
            ),
            usage=UsageServer(hours_life_time=50000),
        )

        server_model = mapper_server(server_dto)

        assert server_model.gpu is not None
        assert (
            server_model.gpu.usage.hours_life_time.value
            == server_model.usage.hours_life_time.value
        )
