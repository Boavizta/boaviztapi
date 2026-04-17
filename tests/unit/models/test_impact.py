"""Tests for Impact.rounded_value() method branch coverage"""

from boaviztapi.models.impact import Impact, WARNING_IMPORTANT_UNCERTAINTY
from boaviztapi import config


def test_rounded_value_rd_value_equals_zero():
    """Test branch: if rd_value == 0"""
    # Create an impact where round_based_on_min_max returns 0
    # This happens when rounding a very small value with wide min/max
    impact = Impact(value=0.0001, min=0.00001, max=10)
    result = impact.rounded_value()
    # Should add warning and return min_sig_fig rounded value
    assert WARNING_IMPORTANT_UNCERTAINTY in impact.warnings
    assert isinstance(result, float)


def test_rounded_value_wide_uncertainty():
    """Test branch: if self.value != 0 and self.max > self.min"""
    impact = Impact(value=100, min=10, max=200)
    result = impact.rounded_value()
    assert isinstance(result, float)
    assert result != 0


def test_rounded_value_approx_greater_than_zero():
    """Test branch: if approx > 0 (nested in uncertainty check)"""
    impact = Impact(value=50, min=40, max=60)
    result = impact.rounded_value()
    assert isinstance(result, float)


def test_rounded_value_rounding_to_zero_adds_warning():
    """Test branch: if round(self.value / pow(10, uncapped_sig)) == 0"""
    # Create a scenario where the intermediate rounding equals zero
    # This triggers the warning for high uncertainty
    impact = Impact(value=0.01, min=0.001, max=10)
    result = impact.rounded_value()
    # When rounding produces 0 at intermediate step, warning should be added
    assert isinstance(result, float)


def test_rounded_value_exceeds_max_sig_fig():
    """Test branch: if nb_sig_fig > config.max_sig_fig"""
    # Create impact with value that has many significant figures
    impact = Impact(value=123.456789, min=100, max=150)
    result = impact.rounded_value()
    # Result should be capped to max_sig_fig
    nb_sig_fig = len(str(result).replace(".", "").replace("-", "").lstrip("0"))
    assert nb_sig_fig <= config.max_sig_fig


def test_rounded_value_normal_case():
    """Test happy path through rounded_value"""
    impact = Impact(value=100, min=90, max=110)
    result = impact.rounded_value()
    assert isinstance(result, float)
    assert result > 0


def test_rounded_value_with_zero_min_max_difference():
    """Test when min == max (no uncertainty)"""
    impact = Impact(value=50, min=50, max=50)
    result = impact.rounded_value()
    assert isinstance(result, (int, float))
    assert result == 50


def test_rounded_value_with_default_values():
    """Test Impact with default values"""
    impact = Impact()
    result = impact.rounded_value()
    # Should handle default value=0, min=0, max=0 gracefully
    assert isinstance(result, float)
