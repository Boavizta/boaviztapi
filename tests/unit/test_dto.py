from boaviztapi.dto.component.gpu import GPU, mapper_gpu


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
