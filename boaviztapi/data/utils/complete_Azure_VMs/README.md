# Completing and updating Azure VMs data

## Source data

1. Get benchmark data matching instance type to physical CPU : https://learn.microsoft.com/en-us/azure/virtual-machines/linux/compute-benchmark-scores and https://learn.microsoft.com/en-us/azure/virtual-machines/windows/compute-benchmark-scores, save as `instances_azure_linux.csv` and `instances_azure_windows.csv`
2. Get dedicated_hosts.csv from https://azure.microsoft.com/en-us/pricing/details/virtual-machines/dedicated-host/ (Copy paste the table in libreoffice benefiting from automatic column filling, remove last two columns "1 year savings plan,3 year savings plan" then export in csv), then run `clean_dedicated_hosts.sh > cleaned_dedicated_hosts.csv`
3. Get Azure VMs data from vantage `azure_vms_from_vantage.csv` from : https://instances.vantage.sh/azure/
4. Get data from tables in each [Dedicated Host documentation page](https://learn.microsoft.com/fr-fr/azure/virtual-machines/dedicated-host-general-purpose-skus) manually (or by scraping, if you wan to contribute), save it as or update `manual_instance_host.csv`

## Workflow

![Updating Azure's data in BoaviztAPI workflow](azure_update_workflow.webp)

## Hypothesis, choices and caveats

- We tried to get the widest instance families coverage possible, mixing data from several places in Microsoft Azure documentation and vantage website. While this seems a nice approach to be as complete as it can be, this may lead to incoherent data and mistakes while mixing data from different source for the same instance or physical host.
- As Microsoft provides "Dedicated Hosts" that you could rent as the hardware platforms of the virtual machines you consume on Azure, we used this list of host as our bare-metal platforms pool, and tried to map each instance to a host at least. When we didn't have an explicit match, we used the CPU reference found in benchmark data for a given instance, to match one of those hosts nevertheless. This probably hides part of the truth behind the scene, as some instances are not explicitely said to be on a given host and we matched them to dedicated hosts anyway.
- 

## TODO

- [ ] GPU allocated to virtual machines are not properly filled, fis this
- [ ] update references count alongside the workflow to identify data losses

## Sources / To-read-list

- [https://azure.microsoft.com/en-us/pricing/details/virtual-machines/series/](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/series/)
- [B series blog post](https://azure.microsoft.com/en-us/blog/introducing-b-series-our-new-burstable-vm-size/)
- [Informations about storage capacity and performance](https://learn.microsoft.com/fr-fr/azure/virtual-machines/disks-scalability-targets)
- [FinOps calculations useful for CPU allocation hypothesis ?](https://singhkays.medium.com/understanding-the-azure-b-series-and-cpu-credits-cd6ad1c46094)
- [List of available dedicated hosts](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/dedicated-host/#resources)