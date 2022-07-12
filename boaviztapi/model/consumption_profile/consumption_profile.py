from abc import abstractmethod, ABC
from pydantic import BaseModel


class Workload(BaseModel):
    pass


class ConsumptionProfile(BaseModel):
    coefs: dict

    @abstractmethod
    def workload_to_power(self, workload: float):
        pass

    @abstractmethod
    def workloads_to_power(self, workload: Workload):
        pass

    @abstractmethod
    def to_json(self):
        pass


class CPUConsumptionProfile(ConsumptionProfile):

    def workloads_to_power(self, workload: Workload):
        pass

    def to_json(self):
        pass

    def workload_to_power(self, workload: float):
        pass
