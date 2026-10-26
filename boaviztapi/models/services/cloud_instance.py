from boaviztapi import config
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.consumption_profile import RAMConsumptionProfileModel
from boaviztapi.models.device.server import (
    DeviceServer,
    disk_power_consumption,
    gpu_power_consumption,
)
from boaviztapi.models.impact import Assessable, ImpactFactor
from boaviztapi.models.usage import ModelUsage
from boaviztapi.data.archetype import (
    get_server_archetype,
    get_cloud_instance_archetype,
    get_arch_value,
)


class Service(Assessable):
    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.units = Boattribute(default=1, min=1, max=1)
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

    def __init__(
        self,
        archetype=get_cloud_instance_archetype(
            config.default_cloud_instance, config.default_cloud_provider
        ),
        **kwargs,
    ):
        super().__init__(archetype=archetype, **kwargs)

        self._platform = DeviceServer(
            archetype=get_server_archetype(
                archetype_name=get_arch_value(archetype, "platform", "default")
            )
        )
        self.vcpu = Boattribute(
            default=get_arch_value(archetype, "vcpu", "default"),
            min=get_arch_value(archetype, "vcpu", "min"),
            max=get_arch_value(archetype, "vcpu", "max"),
        )
        self.memory = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "memory", "default"),
            min=get_arch_value(archetype, "memory", "min"),
            max=get_arch_value(archetype, "memory", "max"),
        )
        self.hdd_storage = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "hdd_storage", "default"),
            min=get_arch_value(archetype, "hdd_storage", "min"),
            max=get_arch_value(archetype, "hdd_storage", "max"),
        )
        self.ssd_storage = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "ssd_storage", "default"),
            min=get_arch_value(archetype, "ssd_storage", "min"),
            max=get_arch_value(archetype, "ssd_storage", "max"),
        )
        self.gpu_units = Boattribute(
            default=get_arch_value(archetype, "gpu_units", "default"),
            min=get_arch_value(archetype, "gpu_units", "min"),
            max=get_arch_value(archetype, "gpu_units", "max"),
        )

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def platform(self) -> DeviceServer:
        if self._platform is None:
            self._platform = DeviceServer(
                archetype=get_server_archetype(
                    archetype_name=self.archetype["platform"]
                )
            )
        return self._platform

    @platform.setter
    def platform(self, value: DeviceServer) -> None:
        self._platform = value

    def model_power_consumption(self):
        vcpu_allocation = self.vcpu.value / self.platform.get_total_vcpu()
        ram_allocation = self.memory.value / self.platform.get_total_memory()

        total_cpu_consumption = self.platform.cpu.model_power_consumption()
        self.platform.cpu.usage.avg_power.set_completed(
            value=total_cpu_consumption.value * vcpu_allocation,
            min=total_cpu_consumption.min * vcpu_allocation,
            max=total_cpu_consumption.max * vcpu_allocation,
        )

        total_conso_ram = ImpactFactor(value=0, min=0, max=0)

        # The DIMM layout of cloud platforms is unknown: assume typical DIMMs
        # for the memory type of the platform's CPU.
        memory_type = RAMConsumptionProfileModel.memory_type_from_cpu_family(
            self.platform.cpu.family.value
        )
        dimm_capacity = RAMConsumptionProfileModel.typical_dimm_capacity[memory_type]

        for ram in self.platform.ram:
            ram_consumption = ram.model_power_consumption(dimm_capacity=dimm_capacity)

            ram.usage.avg_power.set_completed(
                value=ram_consumption.value * ram_allocation,
                min=ram_consumption.min * ram_allocation,
                max=ram_consumption.max * ram_allocation,
            )

            total_conso_ram.value = total_conso_ram.value + ram.usage.avg_power.value
            total_conso_ram.min = total_conso_ram.min + ram.usage.avg_power.min
            total_conso_ram.max = total_conso_ram.max + ram.usage.avg_power.max

        # Local disks are allocated by storage share, as for embedded impacts.
        total_conso_disk = ImpactFactor(value=0, min=0, max=0)
        for disk in self.platform.disk:
            storage = self.ssd_storage if disk.NAME == "SSD" else self.hdd_storage
            platform_capacity = self.platform.get_total_disk_capacity(disk.NAME)
            if not storage.has_value() or not platform_capacity:
                continue
            disk_allocation = storage.value / platform_capacity
            disk_consumption = disk_power_consumption(disk)
            total_conso_disk.value += disk_consumption.value * disk_allocation
            total_conso_disk.min += disk_consumption.min * disk_allocation
            total_conso_disk.max += disk_consumption.max * disk_allocation

        # GPUs are allocated by GPU count, as for embedded impacts.
        total_conso_gpu = ImpactFactor(value=0, min=0, max=0)
        gpu_allocation = self.gpu_allocation()
        if gpu_allocation:
            self.platform.gpu.complete_avg_power()
            total_conso_gpu = gpu_power_consumption(
                self.platform.gpu, self.gpu_units.value
            )

        # Disks and GPUs are added outside other_consumption_ratio, as for
        # servers (see DeviceServer.model_power_consumption).
        return ImpactFactor(
            value=(self.platform.cpu.usage.avg_power.value + total_conso_ram.value)
            * (1 + self.platform.usage.other_consumption_ratio.value)
            + total_conso_disk.value
            + total_conso_gpu.value,
            min=(self.platform.cpu.usage.avg_power.min + total_conso_ram.min)
            * (1 + self.platform.usage.other_consumption_ratio.min)
            + total_conso_disk.min
            + total_conso_gpu.min,
            max=(self.platform.cpu.usage.avg_power.max + total_conso_ram.max)
            * (1 + self.platform.usage.other_consumption_ratio.max)
            + total_conso_disk.max
            + total_conso_gpu.max,
        )

    def gpu_allocation(self) -> float:
        """Share of the platform's GPUs used by the instance, 0 without GPU."""
        total_gpu = self.platform.get_total_gpu()
        if not total_gpu or not self.gpu_units.has_value() or not self.gpu_units.value:
            return 0
        # Fractional for vGPU/MIG-partitioned instances
        return self.gpu_units.value / total_gpu

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
