from boaviztapi.model.impact import Impact
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.allocation import allocate


def test_allocate_():
    usage = ModelUsage(archetype={})
    usage.hours_life_time.value = 2000

    assert allocate(Impact(value=100, min=100, max=100), 2000, usage.hours_life_time) == (100, 100, 100)
    assert allocate(Impact(value=100, min=100, max=100), 1000, usage.hours_life_time) == (50, 50, 50)

    assert allocate(Impact(), 1000, usage.hours_life_time) == (0, 0, 0)
    assert allocate(Impact(), 2000, usage.hours_life_time) == (0, 0, 0)
