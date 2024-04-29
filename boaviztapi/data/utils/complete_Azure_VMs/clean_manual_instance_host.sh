#!/bin/bash

cat manual_instance_host.csv | tr '\200-\377' ' ' | sed "s/,,/,0,/g" | tr "[:upper:]" "[:lower:]" | sed "s/ /_/g" | tr -d " " | sed "s/__/_/g" > manual_instance_host_cleaned.csv
