import os

from boaviztapi import config

# Set test-specific config values that differ from defaults
config.cpu_name_fuzzymatch_threshold = 60
config.default_case = "DEFAULT"
config.default_server = "DEFAULT"
