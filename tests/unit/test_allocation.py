from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.allocation import allocate, Allocation


def test_allocate_():
    usage = ModelUsage(archetype={})
    usage.use_time.value = 1000
    usage.life_time.value = 2000

    assert allocate(100, Allocation.TOTAL, usage.use_time.value, usage.life_time.value) == 100
    assert allocate(100, Allocation.LINEAR, usage.use_time.value, usage.life_time.value) == 50

    assert allocate(0, Allocation.LINEAR, usage.use_time.value, usage.life_time.value) == 0
    assert allocate(0, Allocation.TOTAL, usage.use_time.value, usage.life_time.value) == 0
