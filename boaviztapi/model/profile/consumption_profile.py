class ConsumptionProfile:

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)
        self._workload = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    def consump