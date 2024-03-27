#!/bin/bash

INSTANCES_CSV="instances_azure_linux.csv"
HOSTS_CSV="cleaned_dedicated_hosts.csv"

while read -r line; 
  do  
    sed "s/Standard_\(F\|D\|B\|FX\|L\|DC\)[0-9]*[0-9]/\1/" |
    sed "s/\(Standard_HB120rs_v3\|Standard_HB120-[0-9]*[0-9]rs_v3\)/HBv3/" |
    sed "s/Standard_HB120rs_v2/HBrsv2/" |
    sed "s/Standard_HB60rs/HBS/"| 
    sed "s/Standard_HC44rs/HCS/" | 
    sed "s/Standard_E[0-9]\?[0-9]\?-\?[0-9][0-9]\?i\?/E/" | 
    sed "s/Standard_\(DS\|D\)[0-9]\?[0-9]-\?[0-9]\?/DS/" |
    sed "s/Standard_M[0-9][0-9]\?[0-9]-\?2\?0\?8\?m\?d\?m\?i\?d\?m\?/M/" |
    sed "s/_//" > tmp_instances.csv
  done <"$INSTANCES_CSV" 

while read -r line;
  do
    INSTANCE_NAME=$(cut -d , -f 1)
    printf "%s" "$INSTANCE_NAME" > tmp_instance_names.csv
  done <"$INSTANCES_CSV"
    
paste tmp_instance_names.csv tmp_instances.csv > result_instances.csv   
