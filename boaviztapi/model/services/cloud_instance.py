from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.impact import Assessable
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_server_archetype, get_cloud_instance_archetype, get_arch_value


class Service(Assessable):
    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.archetype = archetype
        self._usage = None
        self._impacts = {}

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

        self._platform = DeviceServer(archetype=get_server_archetype(archetype_name=archetype["platform"]))
        self._vcpu = Boattribute(
            default=get_arch_value(archetype, 'vcpu', 'default'),
            min=get_arch_value(archetype, 'vcpu', 'min'),
            max=get_arch_value(archetype, 'vcpu', 'max')
        )
        self._memory = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'memory', 'default'),
            min=get_arch_value(archetype, 'memory', 'min'),
            max=get_arch_value(archetype, 'memory', 'max')
        )
        self._hdd_storage = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'hdd_storage', 'default'),
            min=get_arch_value(archetype, 'hdd_storage', 'min'),
            max=get_arch_value(archetype, 'hdd_storage', 'max')
        )
        self._ssd_storage = Boattribute(
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
