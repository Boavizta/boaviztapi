from pydantic import BaseModel
from typing import Dict


class ConsumptionProfile(BaseModel):
    param: dict = None

    def workload_to_power(self, workload: float) -> float:
        pass  # TODO : apply the function to "workload"

    def workloads_to_power(self, workloads: Dict[str, float]) -> float:
        power = 0

        for w in workloads.keys():
            power += self.workload_to_power(float(w)) * workloads[w]

        return power

