from boaviztapi.model.component.component import Component


class ComponentAssembly(Component):
    NAME = "ASSEMBLY"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
