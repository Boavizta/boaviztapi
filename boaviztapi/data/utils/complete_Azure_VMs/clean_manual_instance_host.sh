#!/bin/bash

cat manual_instance_host.csv | sed "s/,,/,0,/g" | tr "[:upper:]" "[:lower:]" | sed "s/ /_/g" > manual_instance_host_cleaned.csv
