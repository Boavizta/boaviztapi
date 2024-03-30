#!/bin/bash

INSTANCES_LINUX_CSV="instances_azure_linux.csv"
INSTANCES_WINDOWS_CSV="instances_azure_windows.csv"
HOSTS_CSV="cleaned_dedicated_hosts.csv"

# Sort both CSV files of Linux and Windows instances benchmarks, and making sure of getting 
# unique values.
sort $INSTANCES_LINUX_CSV > tmp_instances_linux_sorted
sort $INSTANCES_WINDOWS_CSV > tmp_instances_windows_sorted
comm -3 tmp_instances_linux_sorted tmp_instances_windows_sorted > tmp_instances_unique.csv 

INSTANCES_CSV="tmp_instances_unique.csv"

# Remove patterns to get instances families matching part of hosts' families names
while IFS="," read -r ; 
  do  
    sed "s/Standard_\(F\|D\|B\|FX\|L\|DC\)[0-9]*[0-9]/\1/" |
    sed "s/Standard_A[0-9]*[m,0-9]/A/" |
    sed "s/\(Standard_HB120rs_v3\|Standard_HB120-[0-9]*[0-9]rs_v3\)/HBv3/" |
    sed "s/Standard_HB120rs_v2/HBrsv2/" |
    sed "s/Standard_HB60rs/HBS/"| 
    sed "s/Standard_HC44rs/HCS/" | 
    sed "s/Standard_E[0-9]\?[0-9]\?-\?[0-9][0-9]\?i\?/E/" | 
    sed "s/Standard_\(DS\|D\)[0-9]\?[0-9]-\?[0-9]\?/DS/" |
    sed "s/Standard_M[0-9][0-9]\?[0-9]-\?2\?0\?8\?m\?d\?m\?i\?d\?m\?/M/" |
    sed "s/_//" |
    sed -e "s/^[[:space:]]*//" > tmp_instances.csv
  done < $INSTANCES_CSV 

# Add leading column with instance name
while IFS="," read -r instance_name _ ;
  do
    printf "%s,\n" "$instance_name" | sed -e "s/^[[:space:]]*//"  >> tmp_instance_names.csv
  done < $INSTANCES_CSV
 
# Join instance name column to instances' CSV file, lowercase everything  
paste -d "" tmp_instance_names.csv tmp_instances.csv | 
sort |
sed "s/(R)//g" |
tr "[:upper:]" "[:lower:]" > tmp_instances_lowercased.csv   

# Add header to instances' CSV file
sed -i '1i instance_name,instance_family,instance_cpu,vcpus,numa_nodes,memory_gb,avg_score,stddev,stddev_percentage,runs' tmp_instances_lowercased.csv
mv tmp_instances_lowercased.csv instances_lowercased.csv

# Lowercase everything in hosts' CSV file, remove patterns in CPU column that do not exist in instances' CSV file
tr "[:upper:]" "[:lower:]" < $HOSTS_CSV | 
sed "s/\(3rd generation \)\|\([0-9].[0-9][0-9] ghz \)\| ([a-z]*)\| ([a-z]* [a-z]*)//g" | 
sed -e "s/^[[:space:]]*//" > hosts_lowercased.csv

# Match instances and hosts CSV files to link instance name to host family
while IFS="," read -r host_family _ _ host_cpu _;
  do
  host=$(printf "%s" "$host_family" | cut -d "-" -f 1)
  
  csvgrep -c instance_family -m "$host" instances_lowercased.csv | 
  # CLEAN CPUS IN HOST CSVS FOR THIS TO MAYBE WORK
  csvgrep -c instance_cpu -r "$host_cpu" >> instances_matched_with_hosts.csv

  done < hosts_lowercased.csv
rm tmp_*

