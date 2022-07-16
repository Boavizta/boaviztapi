import math
from typing import Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from boaviztapi.model.boattribute import Boattribute, Status

_cpu_profile_consumption_df = pd.read_csv('./boaviztapi/data/consumption_profile/cpu/cpu_profile.csv')


class ConsumptionProfileModel:
    pass


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
        self.cpu_manufacturer = Boattribute(
            status=Status.NONE
        )
        self.cpu_model_range = Boattribute(
            status=Status.NONE,
            default=self.DEFAULT_CPU_MODEL_RANGE
        )
        self.workloads = Boattribute(
            status=Status.NONE,
            default=self.DEFAULT_WORKLOADS
        )

    @property
    def list_workloads(self) -> Tuple[List[float], List[float]]:
        load = [item['load'] for item in self.workloads.value]
        power = [item['power'] for item in self.workloads.value]
        return load, power

    def compute_consumption_profile_model(self) -> Dict[str, float]:
        base_model = self.lookup_consumption_profile()

        if base_model is None:
            base_model = self._DEFAULT_MODEL_PARAMS

        if self.workloads is None:
            return base_model

        final_model = self.__compute_model_adaptation(base_model)
        return final_model

    def lookup_consumption_profile(self) -> Optional[Dict[str, float]]:
        sub = _cpu_profile_consumption_df

        if self.cpu_manufacturer is not None:
            tmp = sub[sub['manufacturer'] == self.cpu_manufacturer]
            if len(tmp) > 0:
                sub = tmp.copy()

        if self.cpu_model_range is not None:
            tmp = sub[sub['model_range'] == self.cpu_model_range]
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

    def __compute_model_adaptation(self, base_model: Dict[str, float]) -> Dict[str, float]:
        base_model_list = self.__model_dict_to_list(base_model)
        bounds = self.__adapt_model_bounds(base_model_list)
        x_data, y_data = self.list_workloads
        popt, _ = curve_fit(f=self.__log_model,
                            xdata=x_data,
                            ydata=y_data,
                            p0=base_model_list,
                            bounds=bounds)
        return self.__model_list_to_dict(popt.tolist())

    def __adapt_model_bounds(self, base_model_list: List[float]) -> Tuple[List[float], List[float]]:
        default_lower_bounds, default_upper_bounds = self._DEFAULT_MODEL_BOUNDS
        lower_bounds, upper_bounds = [], []
        for lower_b, upper_b, model_param in zip(default_lower_bounds, default_upper_bounds, base_model_list):
            lower_bounds.append(max(lower_b, model_param - abs(0.5 * model_param)))
            upper_bounds.append(min(upper_b, model_param + abs(1.5 * model_param)))
        return lower_bounds, upper_bounds

    def __model_dict_to_list(self, model: Dict[str, float]) -> List[float]:
        return [model[param_name] for param_name in self._MODEL_PARAM_NAME]

    def __model_list_to_dict(self, model: List[float]) -> Dict[str, float]:
        return {param_name: param for param_name, param in zip(self._MODEL_PARAM_NAME, model)}

    @staticmethod
    def __log_model(x: float, a: float, b: float, c: float, d: float) -> float:
        return a * np.log(b * (x + c)) + d


if __name__ == '__main__':
    cpm = CPUConsumptionProfileModel()
    cpm.workloads.value = [
        {'load': 0., 'power': 58.},
        {'load': 100., 'power': 618.}
    ]
    print(cpm.compute_consumption_profile_model())
