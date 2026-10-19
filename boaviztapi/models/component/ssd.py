import os

import pandas as pd

from boaviztapi import config, data_dir
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component.component import Component
from boaviztapi.data.archetype import get_component_archetype, get_arch_value
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf


class ComponentSSD(Component):
    _ssd_df = pd.read_csv(os.path.join(data_dir, "crowdsourcing/ssd_manufacture.csv"))

    NAME = "SSD"

    __DISK_TYPE = "ssd"

    # Average power per drive in W (value, min, max), independent of workload.
    # Enterprise NVMe drives idle at ~3.5-5 W and average ~8-14 W when active
    # (Samsung PM9A3 datasheet), up to ~20 W; some idle below 2 W (Kanichai,
    # Doekemeijer et al., IISWC 2026). LBNL 2024 uses ~11 W per NVMe drive.
    POWER_PER_DRIVE = (8, 2, 20)

    def __init__(
        self, archetype=get_component_archetype(config.default_ssd, "ssd"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)
        self.manufacturer = Boattribute(
            default=get_arch_value(archetype, "manufacturer", "default"),
            min=get_arch_value(archetype, "manufacturer", "min"),
            max=get_arch_value(archetype, "manufacturer", "max"),
        )
        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "capacity", "default"),
            min=get_arch_value(archetype, "capacity", "min"),
            max=get_arch_value(archetype, "capacity", "max"),
        )
        self.density = Boattribute(
            unit="GB/cm2",
            complete_function=self._complete_density,
            default=get_arch_value(archetype, "density", "default"),
            min=get_arch_value(archetype, "density", "min"),
            max=get_arch_value(archetype, "density", "max"),
        )
        self.layers = Boattribute(
            default=get_arch_value(archetype, "layers", "default"),
            min=get_arch_value(archetype, "layers", "min"),
            max=get_arch_value(archetype, "layers", "max"),
        )

    def _complete_density(self):
        sub = self._ssd_df
        if self.manufacturer.has_value():
            corrected_manufacturer = fuzzymatch_attr_from_pdf(
                self.manufacturer.value, "manufacturer", sub
            )
            if corrected_manufacturer is not None:
                sub = sub[sub["manufacturer"] == corrected_manufacturer]
                if corrected_manufacturer != self.manufacturer.value:
                    self.manufacturer.set_changed(corrected_manufacturer)

        if self.layers.has_value():
            sub = sub[sub["layers"] == self.layers.value]

        if len(sub) == 1:
            self.density.set_completed(
                float(sub["density"]),
                source=str(sub["source"].iloc[0]),
                min=float(sub["density"]),
                max=float(sub["density"]),
            )

        elif (
            len(sub) == 0 or len(sub) == len(self._ssd_df)
        ) and self.density.has_value():
            return

        else:
            self.density.set_completed(
                float(sub["density"].mean()),
                source="Average of " + str(len(sub)) + " rows",
                min=float(sub["density"].min()),
                max=float(sub["density"].max()),
            )
