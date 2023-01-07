class Impact:
    def __init__(self, **kwargs):
        self.value = 0
        self.unit = "none"
        self.error_margin = 0
        self.warnings = []

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    def add_warning(self, warn):
        self.warnings = self.warnings.append(warn)
