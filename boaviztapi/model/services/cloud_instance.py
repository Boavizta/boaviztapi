from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.model.services.cloud_platform import ServiceCloudPlatform
from boaviztapi.model.services.service import Service
from boaviztapi.model.usage.usage import ModelUsageCloudInstance
from boaviztapi.service.archetype import get_cloud_platform_archetype, get_cloud_instance_archetype, get_arch_value




class ServiceCloudInstance(Service):
    NAME = "CLOUD_INSTANCE"

    def __init__(self, archetype=get_cloud_instance_archetype(config["default_cloud_instance"], config["default_cloud_provider"]),
                 **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self._platform = None
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
    def platform(self) -> ServiceCloudPlatform:
        if self._platform is None:
            self._platform = ServiceCloudPlatform(archetype=get_cloud_platform_archetype(archetype_name=get_arch_value(self.archetype,'platform', 'default'),
                                                                                         provider=get_arch_value(self.archetype,'provider', 'default')))
        return self._platform

    @platform.setter
    def platform(self, value: ServiceCloudPlatform) -> None:
        self._platform = value

    @property
    def usage(self) -> ModelUsageCloudInstance:
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageCloudInstance) -> None:
        self._usage = value
        self.platform.usage = self.usage

    def model_power_consumption(self):
        platform_cpu_consumption = self.platform.model_cpu_power_consumption()
        platform_ram_consumption = self.platform.model_ram_power_consumption()

        vcpu_allocation = self.vcpu.value / self.platform.get_total_vcpu()
        ram_allocation = self.memory.value / self.platform.get_total_memory()
        
        instance_cpu_consumption = ImpactFactor(
            value=platform_cpu_consumption.value * vcpu_allocation,
            min=platform_cpu_consumption.min * vcpu_allocation,
            max=platform_cpu_consumption.max * vcpu_allocation,
        )
        instance_ram_consumption = ImpactFactor(
            value=platform_ram_consumption.value * ram_allocation,
            min=platform_ram_consumption.min * ram_allocation,
            max=platform_ram_consumption.max * ram_allocation,
        )

        instance_others_consumption = self.platform.model_others_power_consumption(
            ImpactFactor(
            value=(instance_cpu_consumption.value + instance_ram_consumption.value),
            min=(instance_cpu_consumption.min + instance_ram_consumption.min),
            max=(instance_cpu_consumption.max + instance_ram_consumption.max)
        ))

        

        return ImpactFactor(
            value=(instance_cpu_consumption.value + instance_ram_consumption.value + instance_others_consumption.value),
            min=(instance_cpu_consumption.min + instance_ram_consumption.min + instance_others_consumption.min),
            max=(instance_cpu_consumption.max + instance_ram_consumption.max + instance_others_consumption.max),
        )

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value