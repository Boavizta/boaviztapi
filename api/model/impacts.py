from marshmallow import Schema, fields

@property
class Impact:
    def __init__(self, method, total, manufacturing, use, error_ratio):
        self.method = method
        self.error_ratio = error_ratio
        self.use = use
        self.manufacturing = manufacturing
        self.total = total
        super().__init__()


@property
class Impacts:
    def __init__(self, impacts_list, hypothesis):
        self.hypothesis = hypothesis
        self.impacts_list = impacts_list
        super().__init__()
