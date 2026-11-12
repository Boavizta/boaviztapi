import pytest

from boaviztapi.data.factor_provider import get_gpu_impact_factor, impact_factors

GPU_PHASES = [
    (component, phase)
    for component, phases in impact_factors["gpu"].items()
    for phase in phases
]


class TestGpuImpactFactors:
    @pytest.mark.parametrize(
        "criterion,gpu_key",
        [
            ("gwppb", "gwpb"),
            ("gwppf", "gwpf"),
            ("gwpplu", "gwplu"),
            ("epf", "efp"),
            ("epm", "efm"),
        ],
    )
    def test_api_criterion_reads_gpu_key(self, criterion, gpu_key):
        factor = get_gpu_impact_factor("casing", "manufacture", criterion)
        assert factor == impact_factors["gpu"]["casing"]["manufacture"][gpu_key]

    @pytest.mark.parametrize("component,phase", GPU_PHASES)
    def test_gwp_split_adds_up_to_gwp(self, component, phase):
        def factor(criterion):
            return get_gpu_impact_factor(component, phase, criterion)["impact"]

        split = factor("gwppb") + factor("gwppf") + factor("gwpplu")
        assert split == pytest.approx(factor("gwp"), rel=1e-4)

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
