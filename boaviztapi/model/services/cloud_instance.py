from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.impact import Assessable, ImpactFactor
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_server_archetype, get_cloud_instance_archetype, get_arch_value


class Service(Assessable):
    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.units = Boattribute(
            default=1,
            min=1,
            max=1
        )
        self.archetype = archetype
        self._usage = None
        self._impacts = {}

    @property
    def usage(self) -> ModelUsage:
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value


class ServiceCloudInstance(Service):
    NAME = "CLOUD_INSTANCE"

    def __init__(self, archetype=get_cloud_instance_archetype(config["default_cloud_instance"], config["default_cloud_provider"]),
                 **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self._platform = DeviceServer(archetype=get_server_archetype(archetype_name=get_arch_value(archetype, 'platform', 'default')))
        self.vcpu = Boattribute(
            default=get_arch_value(archetype, 'vcpu', 'default'),
            min=get_arch_value(archetype, 'vcpu', 'min'),
            max=get_arch_value(archetype, 'vcpu', 'max')
        )
        self.memory = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'memory', 'default'),
            min=get_arch_value(archetype, 'memory', 'min'),
            max=get_arch_value(archetype, 'memory', 'max')
        )
        self.hdd_storage = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'hdd_storage', 'default'),
            min=get_arch_value(archetype, 'hdd_storage', 'min'),
            max=get_arch_value(archetype, 'hdd_storage', 'max')
        )
        self.ssd_storage = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'ssd_storage', 'default'),
            min=get_arch_value(archetype, 'ssd_storage', 'min'),
            max=get_arch_value(archetype, 'ssd_storage', 'max')
        )

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def platform(self) -> DeviceServer:
        if self._platform is None:
            self._platform = DeviceServer(archetype=get_server_archetype(archetype_name=self.archetype["platform"]))
        return self._platform

    @platform.setter
    def platform(self, value: DeviceServer) -> None:
        self._platform = value

    def model_power_consumption(self):
        vcpu_allocation = self.vcpu.value / self.platform.get_total_vcpu()
        ram_allocation = self.memory.value / self.platform.get_total_memory()

        total_cpu_consumption = self.platform.cpu.model_power_consumption()
        self.platform.cpu.usage.avg_power.set_completed(value=total_cpu_consumption.value * vcpu_allocation,
                                                        min=total_cpu_consumption.min * vcpu_allocation,
                                                        max=total_cpu_consumption.max * vcpu_allocation)

        total_conso_ram = ImpactFactor(
            value=0,
            min=0,
            max=0
        )

        for ram in self.platform.ram:
            ram_consumption = ram.model_power_consumption()

            ram.usage.avg_power.set_completed(value=ram_consumption.value * ram_allocation,
                                              min=ram_consumption.min * ram_allocation,
                                              max=ram_consumption.max * ram_allocation)

            total_conso_ram.value = total_conso_ram.value + ram.usage.avg_power.value
            total_conso_ram.min = total_conso_ram.min + ram.usage.avg_power.min
            total_conso_ram.max = total_conso_ram.max + ram.usage.avg_power.max

        return ImpactFactor(
            value=(self.platform.cpu.usage.avg_power.value + total_conso_ram.value) * (1 + self.platform.usage.other_consumption_ratio.value),
            min=(self.platform.cpu.usage.avg_power.min + total_conso_ram.min) * (1 + self.platform.usage.other_consumption_ratio.min),
            max=(self.platform.cpu.usage.avg_power.max + total_conso_ram.max) * (1 + self.platform.usage.other_consumption_ratio.max)
        )

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value