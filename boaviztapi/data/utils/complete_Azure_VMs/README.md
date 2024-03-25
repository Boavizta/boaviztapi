# Completing and updating Azure VMs data

## Source data

1. Get benchmark data matching instance type to physical CPU : https://learn.microsoft.com/en-us/azure/virtual-machines/linux/compute-benchmark-scores and https://learn.microsoft.com/en-us/azure/virtual-machines/windows/compute-benchmark-scores, save as instances_azure_linux.csv and instances_azure_windows.csv
2. Get dedicated_hosts.csv from https://azure.microsoft.com/en-us/pricing/details/virtual-machines/dedicated-host/ (Copy paste the table in libreoffice benefiting from automatic column filling, remove last two columns "1 year savings plan,3 year savings plan" then export in csv), then run clean_dedicated_hosts.csv > cleaned_dedicated_hosts.csv
3. Get Azure VMs data from vantage "azure_vms_from_vantage.csv" from : https://instances.vantage.sh/azure/

## TODO

1. match family name in instance name in instance_\* files
2. match family name from step 1 if present in dedicated_hosts
    a. if present
        i. compare CPU from both files, raise warnings if no match
        ii. set VM <-> platform
    b. if not, get CPU and GPU refs from Azure doc (TODO: link to script)
3. in both cases, fill azure_platforms.csv
4. fill data/archetypes/server.csv with azure_platforms.csv
5. generate azure.csv in data/archetypes/cloud/ with data from steps 1 and 2
