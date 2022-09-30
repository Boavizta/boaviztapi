server_impact_by_model_description = "# ✔ ️Server impacts from model name\n" \
                                     "Retrieve the impacts of a given server name (archetype).\n" \
                                     "### Features\n\n" \
                                     "👄 Verbose\n\n" \
                                     "🔃 Auto-complete\n\n" \
                                     "🔨 Manufacture\n\n" \
                                     "🔌 Usage\n\n" \
                                     "📋 Archetype: " \
                                     "Uses the [classic server impacts router]with a pre-registered archetype \n\n" \
                                     "⏬ Allocation"

server_impact_by_config_description = "# ✔️ Server impacts from configuration\n" \
                                      "Retrieve the impacts of a given server configuration.\n" \
                                      "### Features\n\n" \
                                      "👄 Verbose\n\n" \
                                      "🔃 Auto-complete\n\n" \
                                      "🔨 Manufacture\n\n" \
                                      "🔌 Usage\n\n" \
                                      "* ⏺️  Given\n\n" \
                                      "* 📈 Modeled\n\n" \
                                      "📋 Archetype\n\n" \
                                      "⏬ Allocation"

all_default_model_description = "# ✔️ Get all the available server models\n" \
                                "📜 Return the name of all pre-registered server models"

cpu_description = "# ✔ ️CPU impacts from configuration\n" \
                  "### Features\n\n" \
                  "👄 Verbose\n\n" \
                  "🔃 Auto-complete\n\n" \
                  "🔨 Manufacture\n\n" \
                  "<h3>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = ( " \
                  "cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0," \
                  "491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "cpu<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> " \
                  "🔌 Usage\n\n" \
                  "* ⏺️  Given\n\n" \
                  "* 📈 Modeled\n\n" \
                  "⏬ Allocation"

ssd_description = "# ✔ ️SSD impacts from configuration\n" \
                  "### Features\n\n" \
                  "👄 Verbose\n\n" \
                  "🔃 Auto-complete\n\n" \
                  "🔨 Manufacture\n\n" \
                  "<h3>ssd<sub>manuf<sub><em>criteria</em></sub></sub> =  ( ssd<sub>size</sub> " \
                  "ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ssd<sub>manuf_base<sub><em>criteria</em></sub></sub></h3>" \
                  "🔌 Usage\n\n" \
                  "* ⏺️  Given\n\n" \
                  "⏬ Allocation"

hdd_description = "# ✔ ️HDD impacts from configuration\n" \
                  "### Features\n\n" \
                  "👄 Verbose\n\n" \
                  "🔃 Auto-complete\n\n" \
                  "🔨 Manufacture\n\n" \
                  "The impacts values are set by default" \
                  "🔌 Usage\n\n" \
                  "* ⏺️  Given\n\n" \
                  "⏬ Allocation"

ram_description = "# ✔️ RAM impacts from configuration\n" \
                  "### Features\n\n" \
                  "👄 Verbose\n\n" \
                  "🔃 Auto-complete\n\n" \
                  "🔨 Manufacture\n\n" \
                  "<h3>ram<sub>manuf<sub><em>criteria</em></sub></sub> =( ram<sub>size</sub> " \
                  "/ ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ram<sub>manuf_base<sub><em>criteria</em></sub></sub> </h3> " \
                  "🔌 Usage\n\n" \
                  "* ⏺️  Given\n\n" \
                  "* 📈 Modeled\n\n" \
                  "⏬ Allocation"

motherboard_description = "# ✔ ️Motherboard impacts from configuration\n" \
                          "### Features\n\n" \
                          "👄 Verbose\n\n" \
                          "🔃 Auto-complete\n\n" \
                          "🔨 Manufacture\n\n" \
                          "The impacts values are set by default" \
                          "🔌 Usage\n\n" \
                          "* ⏺️  Given\n\n" \
                          "⏬ Allocation"

power_supply_description = "# ✔ ️Power supply impacts from configuration\n" + \
                           "### Features\n\n" \
                           "👄 Verbose\n\n" \
                           "🔃 Auto-complete\n\n" \
                           "🔨 Manufacture\n\n" \
                           "<h3>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>unit<sub>weight</sub></sub>" \
                           " x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h3> " \
                           "🔌 Usage\n\n" \
                           "* ⏺️  Given : shouldn't be used\n\n" \
                           "⏬ Allocation"

case_description = "# ✔ ️Case impacts from configuration\n" \
                   "### Features\n\n" \
                   "👄 Verbose\n\n" \
                   "🔃 Auto-complete\n\n" \
                   "🔨 Manufacture\n\n" \
                   "<h3>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>unit<sub>weight</sub></sub>" \
                   " x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h3> " \
                   "🔌 Usage\n\n" \
                   "* ⏺️  Given : when the enclosure consumes energy \n\n" \
                   "⏬ Allocation"

cloud_aws_description = "# ✔ ️AWS instance impacts from instance type and usage \n" \
                        "Retrieve the impacts of a given AWS instance and usage.\n\n" \
                        "📋 Instance type \n\n" \
                        "AWS name of the chosen instance. You can retrieve the [list here](" \
                        "#/cloud/server_get_all_archetype_name_v1_cloud_all_aws_instances_get).\n" \
                        "### Features\n\n" \
                        "👄 Verbose\n\n" \
                        "🔨 Manufacture\n\n" \
                        "🔌 Usage \n\n" \
                        "* 📈 Modeled\n\n" \
                        "📋 Archetype : The configuration is set by the API, only usage is given by the user\n\n" \
                        "⏬ Allocation"

all_default_aws_instances = "# ✔ ️Get all the available aws instances\n" \
                            "📜 Return the name of all pre-registered aws instances"

country_code = "# ✔ ️Get all the available countries with their trigram code (*usage:{usage_location: 'FRA'}*)\n"
cpu_family = "# ✔ ️Get all the available cpu family in the API (*cpu:{family:'skylake'}*)\n"
cpu_model_range = "# ✔ ️Get all the available cpu family in the API (*cpu:{model_range:'xeon platinum'}*)\n"
ssd_manufacturer = "# ✔ ️Get all the available ssd manufacturer in the API (*ssd:{manufacturer:'samsung'}*)\n"
ram_manufacturer = "# ✔ ️Get all the available ram manufacturer in the API (*ram:{manufacturer:'samsung'}*)\n"
case_type = "# ✔ ️Get all the available case type in the API (*model:{case:'blade'}*)\n"
name_to_cpu = "# ✔ ️Complete a cpu attributes from a cpu name\n"
