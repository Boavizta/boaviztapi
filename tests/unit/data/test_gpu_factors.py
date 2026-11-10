import pytest

from boaviztapi.data.factor_provider import get_gpu_impact_factor


class TestGpuImpactFactors:
    def test_known_criterion_returns_factor(self):
        factor = get_gpu_impact_factor("casing", "manufacture", "gwp")
        assert factor["impact"] == 8.2542

    @pytest.mark.parametrize("criterion", ["adpe", "fw", "fe"])
    def test_criterion_without_gpu_factor_raises(self, criterion):
        with pytest.raises(NotImplementedError):
            get_gpu_impact_factor("casing", "manufacture", criterion)

    def test_unknown_component_raises(self):
        with pytest.raises(NotImplementedError):
            get_gpu_impact_factor("not_a_component", "manufacture", "gwp")
