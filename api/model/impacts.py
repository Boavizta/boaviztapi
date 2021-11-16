from marshmallow import Schema, fields


@property
class Impact:
    def __init__(self):
        pass

    def add_total(self, quantity):
        self.total += quantity


@property
class Impacts:
    def __init__(self, impacts_list, hypothesis):
        self.hypothesis = hypothesis
        self.impacts_list = impacts_list
        super().__init__()
