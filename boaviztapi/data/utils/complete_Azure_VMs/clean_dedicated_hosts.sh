#!/bin/bash

cat dedicated_hosts.csv  | tr -d "\r" | sed 's/hour\n/hour/' | tr -d "®" | tr -d "™"
