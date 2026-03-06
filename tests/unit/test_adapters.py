"""Unit tests for the outbound adapters (Phase 2)."""

from boaviztapi.adapters.outbound.csv_archetype_repository import CsvArchetypeRepository
from boaviztapi.adapters.outbound.yaml_factor_repository import YamlFactorRepository
from boaviztapi.adapters.outbound.csv_component_completer import CsvComponentCompleter
from boaviztapi.core.ports.archetype_repository import ArchetypeRepository
from boaviztapi.core.ports.factor_repository import FactorRepository
from boaviztapi.core.ports.component_completer import ComponentCompleter


class TestCsvArchetypeRepository:
    def setup_method(self):
        self.repo = CsvArchetypeRepository()

    def test_implements_port(self):
        assert isinstance(self.repo, ArchetypeRepository)

    def test_get_server_archetype_known(self):
        result = self.repo.get_server_archetype("dellR740")
        assert isinstance(result, dict)
        assert "CPU" in result

    def test_get_server_archetype_unknown(self):
        result = self.repo.get_server_archetype("does_not_exist_xyz")
        assert result is False

    def test_get_component_archetype_cpu(self):
        result = self.repo.get_component_archetype("DEFAULT", "cpu")
        assert isinstance(result, dict)

    def test_get_user_terminal_archetype(self):
        result = self.repo.get_user_terminal_archetype("laptop-pro-13.3")
        assert isinstance(result, dict) or result is False

    def test_list_cloud_providers(self):
        providers = self.repo.list_cloud_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0

    def test_list_cloud_regions(self):
        regions = self.repo.list_cloud_regions()
        assert isinstance(regions, list)

    def test_get_cloud_region_mapping_unknown(self):
        result = self.repo.get_cloud_region_mapping(
            "unknown_provider", "unknown_region"
        )
        assert result is None


class TestYamlFactorRepository:
    def setup_method(self):
        self.repo = YamlFactorRepository()

    def test_implements_port(self):
        assert isinstance(self.repo, FactorRepository)

    def test_get_impact_factor(self):
        result = self.repo.get_impact_factor("cpu", "gwp")
        assert isinstance(result, dict)

    def test_get_impact_factor_not_found(self):
        try:
            self.repo.get_impact_factor("nonexistent_item", "gwp")
            assert False, "Should have raised NotImplementedError"
        except NotImplementedError:
            pass

    def test_get_electrical_impact_factor(self):
        result = self.repo.get_electrical_impact_factor("FRA", "gwp")
        assert isinstance(result, dict)

    def test_get_electrical_min_max(self):
        result = self.repo.get_electrical_min_max("gwp", "min")
        assert isinstance(result, (int, float))

    def test_get_available_countries(self):
        countries = self.repo.get_available_countries()
        assert isinstance(countries, dict)
        assert len(countries) > 0

    def test_get_available_countries_reverse(self):
        countries = self.repo.get_available_countries(reverse=True)
        assert isinstance(countries, dict)


class TestCsvComponentCompleter:
    def setup_method(self):
        self.completer = CsvComponentCompleter()

    def test_implements_port(self):
        assert isinstance(self.completer, ComponentCompleter)

    def test_complete_cpu_from_name_known(self):
        result = self.completer.complete_cpu_from_name("Intel Xeon Gold 6134")
        assert result is not None
        assert "name" in result
        assert "manufacturer" in result
        assert "tdp" in result
        assert "core_units" in result
        assert "source" in result

    def test_complete_cpu_from_name_unknown(self):
        result = self.completer.complete_cpu_from_name("zzz_no_such_cpu_xyz")
        assert result is None

    def test_complete_ram_density(self):
        result = self.completer.complete_ram_density(manufacturer="Samsung")
        assert result is not None
        assert "density" in result
        assert "min" in result
        assert "max" in result

    def test_complete_ram_density_no_match(self):
        result = self.completer.complete_ram_density()
        assert result is None

    def test_complete_ssd_density(self):
        result = self.completer.complete_ssd_density(manufacturer="Samsung")
        assert result is not None
        assert "density" in result
        assert "min" in result
        assert "max" in result

    def test_complete_ssd_density_no_match(self):
        result = self.completer.complete_ssd_density()
        assert result is None

    def test_get_cpu_consumption_profile_known(self):
        result = self.completer.get_cpu_consumption_profile(
            cpu_manufacturer="Intel", cpu_model_range="Xeon Gold"
        )
        if result is not None:
            assert "a" in result
            assert "b" in result
            assert "c" in result
            assert "d" in result

    def test_get_cpu_consumption_profile_no_match(self):
        result = self.completer.get_cpu_consumption_profile(
            cpu_manufacturer="zzz_no_such_manufacturer"
        )
        assert result is None
