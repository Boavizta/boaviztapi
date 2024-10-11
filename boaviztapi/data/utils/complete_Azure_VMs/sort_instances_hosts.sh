#!/bin/bash

set -o nounset
set -o noclobber
export LC_ALL=C
export PATH="/bin:/sbin:/usr/bin:/usr/sbin:$PATH"
PS4=' ${BASH_SOURCE##*/}:$LINENO ${FUNCNAME:-main}) '

typeset INSTANCES_LINUX_CSV="instances_azure_linux.csv"
typeset INSTANCES_WINDOWS_CSV="instances_azure_windows.csv"
typeset HOSTS_CSV="cleaned_dedicated_hosts.csv"

typeset REQUIRED_PYTHON="python3"
typeset REQUIRED_CSVKIT="csvgrep csvcut"

if ! command -v ${REQUIRED_PYTHON} &> /dev/null
  then
    printf "%s\n" "Python does not seem available, and is required for csvgrep and csvcut"
    exit 1
fi

typeset csvprogram
for csvprogram in $REQUIRED_CSVKIT; do
  if ! command -v "${csvprogram}" &> /dev/null
    then
      printf "%s\n" "${csvprogram} does not seem available, and is required for this script."
      printf "%s" "Suggestion: install csvkit with pip install csvkit"
      exit 1
  fi
done
 
# Sort both CSV files of Linux and Windows instances benchmarks, and making sure of getting 
# unique values.
sort <(tail -n +2 ${INSTANCES_LINUX_CSV}) >| tmp_instances_linux_sorted
sort <(tail -n +2 "${INSTANCES_WINDOWS_CSV}") >| tmp_instances_windows_sorted
comm -3 tmp_instances_linux_sorted tmp_instances_windows_sorted | 
sed "s/^[[:space:]]*//" >| tmp_instances_unique.csv 

typeset INSTANCES_CSV="tmp_instances_unique.csv"

# Remove patterns to get instances families matching part of hosts' families names
while IFS="," read -r instance_name restofline ; 
  do
    printf "%s, %s\n" "${instance_name}" "${restofline}" |
    sed "s/Standard_\(F\|D\|FX\|L\|DC\)[0-9]*[0-9]/\1/" |
    sed "s/^Standard_B[^,]*/Bseries/" |
    sed "s/Standard_A[0-9]*[m,0-9]/A/" |
    sed "s/\(Standard_HB120rs_v3\|Standard_HB120-[0-9]*[0-9]rs_v3\)/HBv3/" |
    sed "s/Standard_HB120rs_v2/HBrsv2/" |
    sed "s/Standard_HB60rs/HBS/"| 
    sed "s/Standard_HC44rs/HCS/" | 
    sed "s/Standard_E[0-9]\?[0-9]\?-\?[0-9][0-9]\?i\?/E/" | 
    sed "s/Standard_\(DS\|D\)[0-9]\?[0-9]-\?[0-9]\?/DS/" |
    sed "s/(R)//g" |
    sed "s/_//" >> tmp_instances.csv
  done < <(tail -n +1 ${INSTANCES_CSV})

# Add leading column with instance name
while IFS="," read -r instance_name _ ;
  do
    printf "%s,\n" "$instance_name" | sed -e "s/^[[:space:]]*//"  >> tmp_instance_names.csv
  done < <(tail -n +1 ${INSTANCES_CSV})
 
# Join instance name column to instances' CSV file, remove M series instances treated in m_series_host_instances.csv, lowercase everything  
paste -d "" tmp_instance_names.csv tmp_instances.csv | 
sort |
sed "/^Standard_M[^,]*/d" |
tr "[:upper:]" "[:lower:]" >| tmp_instances_lowercased_headless.csv   

# Add header to instances' CSV file
sed -i '1i instance_name,instance_family,instance_cpu,vcpus,numa_nodes,memory_gb,avg_score,stddev,stddev_percentage,runs' tmp_instances_lowercased_headless.csv
mv tmp_instances_lowercased_headless.csv tmp_instances_lowercased.csv

# Lowercase everything in hosts' CSV file, remove patterns in CPU column that do not exist in instances' CSV file
tr "[:upper:]" "[:lower:]" < "${HOSTS_CSV}" | 
sed "s/\(3rd generation \)\|\([0-9].[0-9][0-9] ghz \)\| ([a-z]*)\| ([a-z]* [a-z]*)\|\( processor with sgx technology\)//g" | 
sed "s/\(\".*\"\)/ram/" >| tmp_hosts_lowercased.csv

# Match instances and hosts CSV files to link instance name to host family.
# Av2 and B VM series : ddsv4-type1 as host is an arbitrary choice as only this host is documented
# with Intel Xeon Platinum 8272CL ; other possible CPUs for these series are not presently documented.
# M Series VMs : range of possible hosts is given, as min:avg:max, as multiple CPU possibilities are documented.

while IFS="," read -r host _ _ host_cpu _;
  do
  host_family="$(printf "%s" "${host}" | cut -d "-" -f 1)"

  csvgrep -c instance_family -r "mseries|av2|bseries|${host_family}" tmp_instances_lowercased.csv | 
  csvgrep -c instance_cpu -r "${host_cpu}" | 
  csvformat -E |
  sed "s/${host_family}/${host}/" |
  sed "s/\(av2\|bseries\)/ddsv4-type1/" >> tmp_instances_matched_with_hosts.csv

done < <(tail -n +2 tmp_hosts_lowercased.csv) 

# Scraped data for M series from Memory Optimized SKUs page : https://learn.microsoft.com/en-us/azure/virtual-machines/dedicated-host-memory-optimized-skus
csvcut -c 1,2 tmp_instances_matched_with_hosts.csv >| tmp_instance_host_from_matching.csv
cat tmp_instance_host_from_matching.csv m_series_host_instances.csv | sed "s/ /_/g" >| instance_host.csv

# Generate file with unmatched instances from benchmarks based on instance_host.csv

comm -2 -3  <(cut -d "," -f 1 tmp_instances_lowercased.csv | sed -e "s/^[[:space:]]*//" | sort -u) <(cut -d "," -f 1 instance_host.csv | sed -e "s/^[[:space:]]*//" | sort -u) >| tmp_instance_names_unique_in_benchmarks.csv 

 while IFS="," read -r unmatched_instance_name ;
   do
     csvgrep -c instance_name -m "${unmatched_instance_name}" tmp_instances_lowercased.csv |
     csvformat -E |
     csvcut -c 1,3 |
     sed "s/\([0-9][0-9]-core.*\)\|\(v[0-9] @.*\)\|\(@.*\)//" |
     sort -u >> benchmarked_instances_unmatched.csv
   done < tmp_instance_names_unique_in_benchmarks.csv 

rm tmp_*
