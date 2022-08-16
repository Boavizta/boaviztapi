import math
from typing import Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from boaviztapi.dto.usage.usage import WorkloadTime
from boaviztapi.model.boattribute import Boattribute, Status

_cpu_profile_consumption_df = pd.read_csv('./boaviztapi/data/consumption_profile/cpu/cpu_profile.csv')


class ConsumptionProfileModel:
    pass


def lookup_consumption_profile(cpu_manufacturer, cpu_model_range) -> Optional[Dict[str, float]]:
    sub = _cpu_profile_consumption_df

    if cpu_manufacturer is not None:
        tmp = sub[sub['manufacturer'] == cpu_manufacturer]
        if len(tmp) > 0:
            sub = tmp.copy()

    if cpu_model_range is not None:
        tmp = sub[sub['model_range'] == cpu_model_range]
        if len(tmp) > 0:
            sub = tmp.copy()

    if len(sub) == 1:
        row = sub.iloc[0]
        return {
            'a': row.a,
            'b': row.b,
            'c': row.c,
            'd': row.d,
        }


class CPUConsumptionProfileModel(ConsumptionProfileModel):
    DEFAULT_CPU_MODEL_RANGE = 'Xeon Platinum'
    DEFAULT_WORKLOADS = None

    _DEFAULT_MODEL_PARAMS = {
        'a': 342.4,
        'b': 0.0347,
        'c': 36.89,
        'd': -16.40
    }
    _DEFAULT_MODEL_BOUNDS = (
        [0, 0, 0, -math.inf],
        [math.inf, math.inf, math.inf, math.inf]
    )
    _MODEL_PARAM_NAME = ['a', 'b', 'c', 'd']

    def __init__(self):
        self.power_workloads = Boattribute(
            status=Status.NONE,
            default=self.DEFAULT_WORKLOADS,
            unit="workload_rate:W"
        )
        self.params = Boattribute(
            status=Status.NONE,
            default=self._DEFAULT_MODEL_PARAMS
        )

    @property
    def list_workloads(self) -> Tuple[List[float], List[float]]:
        load = [item.load for item in self.power_workloads.value]
        power = [item.power for item in self.power_workloads.value]
        return load, power

    def compute_consumption_profile_model(self, cpu_manufacturer, cpu_model_range) -> Dict[str, float]:
        base_model = lookup_consumption_profile(cpu_manufacturer, cpu_model_range)

        if base_model is None:
            base_model = self._DEFAULT_MODEL_PARAMS

        if self.power_workloads.value is None:
            return base_model

        final_model = self.__compute_model_adaptation(base_model)

        self.params.value = final_model
        self.params.status = Status.COMPLETED

        return self.params.value

    def apply_consumption_profile(self, x: float):
        return self.__log_model(x, self.params.value['a'], self.params.value['b'], self.params.value['c'], self.params.value['d'])

    def apply_multiple_workloads(self, time_workload: List[WorkloadTime]):
        total = 0
        for workload in time_workload:
            total += workload.time * self.apply_consumption_profile(workload.load)
        return total

    def __compute_model_adaptation(self, base_model: Dict[str, float]) -> Dict[str, float]:
        base_model_list = self.__model_dict_to_list(base_model)
        x_data, y_data = self.list_workloads
        popt, _ = curve_fit(f=self.__log_model,
                            xdata=x_data,
                            ydata=y_data,
                            p0=base_model_list,
                            bounds=self._DEFAULT_MODEL_BOUNDS)
        return self.__model_list_to_dict(popt.tolist())

    def __model_dict_to_list(self, model: Dict[str, float]) -> List[float]:
        return [model[model_name] for model_name in self._MODEL_PARAM_NAME]

    def __model_list_to_dict(self, model: List[float]) -> Dict[str, float]:
        return {model_name: param for model_name, param in zip(self._MODEL_PARAM_NAME, model)}

    @staticmethod
    def __log_model(x: float, a: float, b: float, c: float, d: float) -> float:
        return a * np.log(b * (x + c)) + d


if __name__ == '__main__':
    cpm = CPUConsumptionProfileModel()
    cpm.power_workloads.value = [
        {'load': 0., 'power': 58.},
        {'load': 100., 'power': 618.}
    ]
    print(cpm.compute_consumption_profile_model())
