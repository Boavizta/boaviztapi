from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.model.services.service import Service
from boaviztapi.model.usage.usage import ModelUsage
from boaviztapi.service.archetype import get_server_archetype, get_cloud_platform_archetype, get_arch_value




class ServiceCloudPlatform(Service):
    NAME = "CLOUD_PLATFORM"

    def __init__(self, archetype=get_cloud_platform_archetype(archetype_name=config["default_cloud_platform"],provider=config["default_cloud_provider"]),
                 **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self._server = DeviceServer(archetype=get_server_archetype(archetype_name=get_arch_value(archetype, 'server_id', 'default')))
        self.server_quantity = get_arch_value(archetype, 'servers_quantity', 'default')
        self._pue = get_arch_value(archetype, 'PUE', 'default')

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def server(self) -> DeviceServer:
        if self._server is None:
            self._server = DeviceServer(archetype=get_server_archetype(archetype_name=self.archetype["server_id"]))
        return self._server

    @server.setter
    def server(self, value: DeviceServer) -> None:
        self._server = value

    @property
    def usage(self) -> ModelUsage:
        return self._usage
    
    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value
        self._server.usage = self.usage

    def model_power_consumption(self):
        cpu_consumption = self.model_cpu_power_consumption()
        ram_consumption = self.model_ram_power_consumption()

        others_consumption = self.model_others_power_consumption(
            ImpactFactor(
            value=(cpu_consumption.value + ram_consumption.value),
            min=(cpu_consumption.min + ram_consumption.min),
            max=(cpu_consumption.max + ram_consumption.max)
        ))
        
        return ImpactFactor(
            value=(cpu_consumption.value + ram_consumption.value + others_consumption.value),
            min=(cpu_consumption.min + ram_consumption.min + others_consumption.min),
            max=(cpu_consumption.max + ram_consumption.max + others_consumption.max)
        )
        # TODO vérifier, il manque la conso des disques?

    def model_cpu_power_consumption(self) -> ImpactFactor:
        total_cpu_consumption = self.server.cpu.model_power_consumption()
        return ImpactFactor(value=total_cpu_consumption.value * self.server_quantity * self._pue,
                            min=total_cpu_consumption.min * self.server_quantity * self._pue,
                            max=total_cpu_consumption.max * self.server_quantity * self._pue)

    def model_ram_power_consumption(self) -> ImpactFactor:
        total_conso_ram = ImpactFactor(
            value=0,
            min=0,
            max=0
        )

        for ram in self.server.ram:
            ram_consumption = ram.model_power_consumption()

            ram.usage.avg_power.set_completed(value=ram_consumption.value * self.server_quantity * self._pue,
                                              min=ram_consumption.min * self.server_quantity * self._pue,
                                              max=ram_consumption.max * self.server_quantity * self._pue)

            total_conso_ram.value += ram_consumption.value * self.server_quantity * self._pue
            total_conso_ram.min += ram_consumption.min * self.server_quantity * self._pue
            total_conso_ram.max += ram_consumption.max * self.server_quantity * self._pue
        return total_conso_ram
    
    def model_others_power_consumption(self, rest_consumption: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=rest_consumption.value * self.server.usage.other_consumption_ratio.value,
            min=rest_consumption.min * self.server.usage.other_consumption_ratio.min,
            max=rest_consumption.max * self.server.usage.other_consumption_ratio.max
        )

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def get_total_vcpu(self):
        return self.server.get_total_vcpu() * self.server_quantity
    
    def get_total_disk_capacity(self, disk_type):
        return self.server.get_total_disk_capacity(disk_type) * self.server_quantity
    
    def get_total_memory(self):
        return self.server.get_total_memory() * self.server_quantity
    
    def get_components(self):
        return self.server.components