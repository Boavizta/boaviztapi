from marshmallow import Schema, fields


class Impact:
    def __init__(self):
        self.total = 0
        pass

    def add_total(self, quantity):
        self.total += quantity


class Impacts:
    def __init__(self, impacts_list, hypothesis):
        self.hypothesis = hypothesis
        self.impacts_list = impacts_list
        super().__init__()

    def to_json(self):
        impact_dict = {"impacts": {}, "hypothesis": ""}
        for impact in self.impacts_list:
            impact_dict["impacts"][impact] = self.impacts_list[impact].total
            impact_dict["hypothesis"] = self.hypothesis
        return impact_dict
