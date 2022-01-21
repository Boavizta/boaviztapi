from boaviztapi.service.verbose import verbose_component, verbose_device


def test_verbose_component_cpu(empty_cpu, complete_cpu):
    assert verbose_component(complete_cpu, empty_cpu) == {
        'core_units': {'input_value': None, 'status': 'SET', 'used_value': 12},
        'die_size_per_core': {'input_value': None, 'status': 'SET', 'used_value': 0.245},
        'impacts': {'adp': 0.02, 'gwp': 16.0, 'pe': 247.0}}


def test_verbose_component_ram(empty_ram, complete_ram):
    assert verbose_component(complete_ram, empty_ram) == {
        'capacity': {'input_value': None, 'used_value': 32, 'status': 'SET'},
        'density': {'input_value': None, 'used_value': 1.79, 'status': 'SET'},
        'impacts': {'gwp': 45.0, 'pe': 562.0, 'adp': 0.003}}


def test_verbose_component_ssd(empty_ssd, complete_ssd):
    assert verbose_component(complete_ssd, empty_ssd) == {
        'capacity': {'input_value': None, 'used_value': 400, 'status': 'SET'},
        'density': {'input_value': None, 'used_value': 50.6, 'status': 'SET'},
        'impacts': {'gwp': 24.0, 'pe': 293.0, 'adp': 0.001}}


def test_verbose_component_power_supply(empty_power_supply, complete_power_supply):
    assert verbose_component(complete_power_supply, empty_power_supply) == {
        'unit_weight': {'input_value': None, 'used_value': 2.0, 'status': 'SET'},
        'impacts': {'gwp': 49.0, 'pe': 704.0, 'adp': 0.017}}


def test_verbose_device_server_1(empty_server, dell_r740):
    print(verbose_device(dell_r740, empty_server))
    assert verbose_device(dell_r740, empty_server) == {
        'CPU-1': {
            'unit': 2, 'hash': '5f75d18d9165b04381f24cb2130b62f756d266c45080982334585931482398ad',
            'core_units': {'input_value': None, 'used_value': 24, 'status': 'SET'},
            'die_size_per_core': {'input_value': None, 'used_value': 0.245, 'status': 'SET'},
            'impacts': {'gwp': 44.0, 'pe': 650.0, 'adp': 0.04}},
        'RAM-1': {'unit': 12, 'hash': '4985faa0d798469b3deea291f6e9852862e43a06f5364164e57801035cfa3410',
                  'capacity': {'input_value': None, 'used_value': 32, 'status': 'SET'},
                  'density': {'input_value': None, 'used_value': 1.79, 'status': 'SET'},
                  'impacts': {'gwp': 540.0, 'pe': 6744.0, 'adp': 0.036}},
        'SSD-1': {'unit': 1, 'hash': '41514f07d8fa09207407a0693c20b7647cba1751e658999a51b4c003fc032c91',
                  'capacity': {'input_value': None, 'used_value': 400, 'status': 'SET'},
                  'density': {'input_value': None, 'used_value': 50.6, 'status': 'SET'},
                  'impacts': {'gwp': 24.0, 'pe': 293.0, 'adp': 0.001}},
        'POWER_SUPPLY-1': {'unit': 2, 'hash': 'cdb1c15f77554bf77b8d8ccc2094af7ed72a8a19ff3f0fd0a9909ecacec06428',
                           'unit_weight': {'input_value': None, 'used_value': 2.99, 'status': 'SET'},
                           'impacts': {'gwp': 146.0, 'pe': 2104.0, 'adp': 0.05}},
        'RACK-1': {'unit': 1, 'hash': '31990b3599a2a7bca40559e28c3d99670ab75f5a71d121cb60b867e81a1fb0f7',
                   'impacts': {'gwp': 150.0, 'pe': 2200.0, 'adp': 0.02}}}


def test_verbose_device_server_2(incomplete_server, completed_server):
    assert verbose_device(completed_server, incomplete_server) == {
        'RAM-1': {'unit': 24, 'hash': '4985faa0d798469b3deea291f6e9852862e43a06f5364164e57801035cfa3410',
                  'capacity': {'input_value': 32, 'used_value': 32, 'status': 'UNCHANGED'},
                  'density': {'input_value': 1.79, 'used_value': 1.79, 'status': 'UNCHANGED'},
                  'impacts': {'gwp': 1080.0, 'pe': 13488.0, 'adp': 0.072}},
        'SSD-1': {'unit': 2, 'hash': '41514f07d8fa09207407a0693c20b7647cba1751e658999a51b4c003fc032c91',
                  'capacity': {'input_value': 400, 'used_value': 400, 'status': 'UNCHANGED'},
                  'density': {'input_value': 50.6, 'used_value': 50.6, 'status': 'UNCHANGED'},
                  'impacts': {'gwp': 48.0, 'pe': 586.0, 'adp': 0.002}},
        'BLADE-1': {'unit': 1, 'hash': 'b0e1b5a120eaf28e9610d1cc00fa34dda951201039d0e0d1628ab12bd266b51c',
                    'impacts': {'gwp': 86.0, 'pe': 1229.0, 'adp': 0.028}},
        'MOTHERBOARD-1': {'unit': 1, 'hash': '3a31a8fbd4b871719831ef11af93eefbb1c2afc0f62d850a31fb5475aac9336e',
                          'impacts': {'gwp': 66.0, 'pe': 836.0, 'adp': 0.004}},
        'ASSEMBLY-1': {'unit': 1, 'hash': '8bfe70a2b59691c050865455cc9cf1b561ec702e7cf930c1026a490964bbd364',
                       'impacts': {'gwp': 7.0, 'pe': 69.0, 'adp': 0.0}},
        'CPU-1': {'unit': 2, 'hash':  'c8c7d224967280c8cb4cb95bfc1727e68645f38154310d2f8091170915f49464',
                  'core_units': {'input_value': None, 'used_value': 24, 'status': 'SET'},
                  'die_size_per_core': {'input_value': None, 'used_value': 0.245, 'status': 'SET'},
                  'impacts': {'gwp': 44.0, 'pe': 650.0, 'adp': 0.04}},
        'POWER_SUPPLY-1': {'unit': 2, 'hash': 'be84aabaaac41126e1bd93ec3c10b355c6c7534cf9e3d7337cef9d6d0bb116c6',
                           'unit_weight': {'input_value': None, 'used_value': 2.99, 'status': 'SET'},
                           'impacts': {'gwp': 146.0, 'pe': 2104.0, 'adp': 0.05}}}

