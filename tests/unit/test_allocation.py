from boaviztapi.model.impact import Impact
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.allocation import allocate


def test_allocate_():
    usage = ModelUsage(archetype={})
    duration = 1000
    usage.life_time.value = 2000

    assert allocate(Impact(value=100, min=100, max=100), duration, usage.life_time) == (100, 100, 100)
    assert allocate(Impact(value=100, min=100, max=100), duration, usage.life_time) == (50, 50, 50)

    assert allocate(Impact(), duration, usage.life_time) == (0,0,0)
    assert allocate(Impact(), duration, usage.life_time) == (0,0,0)
