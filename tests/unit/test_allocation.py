from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.allocation import allocate, Allocation


def test_allocate_():
    usage = ModelUsage()
    usage.use_time.value = 1000
    usage.life_time.value = 2000

    assert allocate(100, Allocation.TOTAL, usage) == 100
    assert allocate(100, Allocation.LINEAR, usage) == 50

    assert allocate(0, Allocation.LINEAR, usage) == 0
    assert allocate(0, Allocation.TOTAL, usage) == 0
