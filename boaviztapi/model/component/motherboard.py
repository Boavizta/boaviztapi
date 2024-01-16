from boaviztapi.model.component.component import Component


class ComponentMotherboard(Component):
    NAME = "MOTHERBOARD"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
