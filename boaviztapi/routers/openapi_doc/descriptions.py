server_impact_by_model_description = "# ✔️Server impacts from model name\n" \
                                     "Retrieve the impacts of a given server name (archetype).\n"\
                                     "### 📋 Model\n" \
                                     "Uses the [classic server impacts router](" \
                                     "#/server/server_impact_by_config_v1_server__post) with a pre-registered model \n" \
                                     "### 👄 Verbose\n" \
                                     "If set at true, shows the impacts of each components and the value used for each " \
                                     "attributes \n " \
                                     "### 📋 Model name\n" \
                                     "You can have a list of available server models names [here](" \
                                     "#/server/server_get_all_archetype_name_v1_server_all_default_models_get)\n " \
                                     "\n### 🧮 Measure\n" \
                                     "🔨 Manufacture impacts are the sum of the pre-registered components impacts\n\n" \
                                     "🔌 Usage impacts are measured based on the electrical consumption of the " \
                                     "pre-registered model for a year "

server_impact_by_config_description = "# ✔️Server impacts from configuration\n" \
                                      "Retrieve the impacts of a given server configuration.\n" \
                                      "### 💡 Smart complete\n" \
                                      "All missing components and components attributes are retrieve with the closest available values. If no data are " \
                                      "available default maximizing data are used\n " \
                                      "### 👄 Verbose\n" \
                                      "If set at true, shows the impacts of each components and the value used for each " \
                                      "attributes \n " \
                                      "### 📋 Archetype\n" \
                                      "An archetype is a pre-registered server model. An ```archetype``` can be " \
                                      "specify in the model object. In case an archetype is specified, " \
                                      "all missing data are retrieve from the archetype. You can have a list of " \
                                      "available archetype's server models [here](" \
                                      "#/server/server_get_all_archetype_name_v1_server_all_default_models_get)\n " \
                                      "\n### ⏲ Duration\n" \
                                      "Usage impacts are given for a specific time duration. Duration can be given in :\n" \
                                      "| time unit | Usage parameter |\n" \
                                      "|------|-----|\n" \
                                      "| HOURS | ```hours_use_time``` |\n" \
                                      "| DAYS | ```days_use_time``` |\n" \
                                      "| YEARS | ```years_use_time``` |\n" \
                                      "If no duration is given, **the impact is measured for a year**.\n" \
                                      "*Note* : units are cumulative" \
                                      "\n### 🧮 Measure\n" \
                                      "🔨 Manufacture impacts are the sum of the components impacts\n\n" \
                                      "🔌 Usage impacts are measured by multiplying :\n" \
                                      "* a **duration**\n\n" \
                                      "* an **impact factor** (```gwp_factor```, ```pe_factor```, ```adp_factor```) - retrieve with ```usage_location``` if not given\n\n" \
                                      "* an **electrical consumption** (```hours_electrical_consumption```) - retrieve with ```workload``` if not given"

all_default_model_description = "# ✔️Get all the available server models\n" \
                                "Return the name of all pre-registered server models"

components_description = "### 💡 Smart complete\n" \
                         "All missing data are retrieve with the closest available values. If no data are " \
                         "available default maximizing data are used\n " \
                         "### 👄 Verbose\n" \
                         "If set at true, shows the the values used for each attribute" \
                         "*Components have no units since they represent a single instance of a component.*"

default_calculation = "\n### 🧮 Measure\n" \
                      "The impacts values are set by default"

cpu_description = "# ✔️CPU impacts from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = ( " \
                  "cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0," \
                  "491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "cpu<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> "

ssd_description = "# ✔️SSD impacts from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>ssd<sub>manuf<sub><em>criteria</em></sub></sub> =  ( ssd<sub>size</sub> " \
                  "ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ssd<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> "

hdd_description = "# ✔️HDD impacts from configuration\n" + components_description + default_calculation

ram_description = "# ✔️RAM impacts from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>ram<sub>manuf<sub><em>criteria</em></sub></sub> =( ram<sub>size</sub> " \
                  "/ ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ram<sub>manuf_base<sub><em>criteria</em></sub></sub> </h3> "

motherboard_description = "# ✔️Motherboard impacts from configuration\n" + components_description + default_calculation

power_supply_description = "# ✔️Power supply impacts from configuration\n" + components_description + \
                           "\n### 🧮 Measure\n" + \
                           "<h3>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>unit<sub>weight</sub></sub>" \
                           " x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h3> "

case_description = "# ✔️Case impacts from configuration\n" + components_description + default_calculation

cloud_aws_description = "# ✔️AWS instance impacts from instance type and usage \n" \
                        "### 📋 Instance type \n" \
                        "AWS name of the chosen instance. You can retrieve the [list here](#/cloud/server_get_all_archetype_name_v1_cloud_all_aws_instances_get).\n" \
                        "### 👄 Verbose\n" \
                        "If set at true, shows the impacts of each components and the value used for each " \
                        "attributes \n " \
                        "\n### ⏲ Duration\n" \
                        "Usage impacts are given for a specific time duration. Duration can be given :\n" \
                        "| time unit | Usage parameter |\n" \
                        "|------|-----|\n" \
                        "| HOURS | ```hours_use_time``` |\n" \
                        "| DAYS | ```days_use_time``` |\n" \
                        "| YEARS | ```years_use_time``` |\n" \
                        "*Note* : units are cumulative\n" \
                        "### 🧮 Measure \n" \
                        "🔨 Manufacture impacts are the sum of the pre-registered components impacts divided by the number of instances host in the physicall server\n\n" \
                        "🔌 Usage impacts are measured by multiplying :\n" \
                        "* a **duration**\n\n" \
                        "* an **impact factor** (```gwp_factor```, ```pe_factor```, ```adp_factor```) - retrieve with ```usage_location``` if not given\n\n" \
                        "* The ```time``` per load in ```workload``` object. The ```power``` per load is retreive from the ```instance_type```"

all_default_aws_instances = "# ✔️Get all the available aws instances\n" \
                                "Return the name of all pre-registered aws instances"
