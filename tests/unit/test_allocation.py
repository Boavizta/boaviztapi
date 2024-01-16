from boaviztapi.model.component import Component
from boaviztapi.model.impact import Impact
from boaviztapi.model.usage import ModelUsage


def test_allocate_():
    component = Component()
    component.usage = ModelUsage(archetype={})
    component.usage.hours_life_time.value = 2000

    i1 = Impact(value=100, min=100, max=100)
    i1.allocate(2000, component.usage.hours_life_time)
    i2 = Impact(value=100, min=100, max=100)
    i2.allocate(1000, component.usage.hours_life_time)
    i3 = Impact()
    i3.allocate(2000, component.usage.hours_life_time)
    i4 = Impact(value=100, min=100, max=100)
    i4.allocate(4000, component.usage.hours_life_time)

    assert i1.value == 100
    assert i2.value == 50
    assert i3.value == 0
    assert i4.value == 100
