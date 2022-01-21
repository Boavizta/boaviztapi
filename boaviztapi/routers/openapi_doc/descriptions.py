server_impact_by_model_description = "# ✔️Server impacts from model name\n" \
                                     "Retrieve the impacts of a given server name. Support manufacture *(GWP, PE, " \
                                     "ADP)* and usage *(GWP)* impacts.\n" \
                                     "### 💡 Smart complete\n" \
                                     "All missing data are retrieve with the closest available values. If no data are " \
                                     "available default maximizing data are used\n " \
                                     "### 👄 Verbose\n" \
                                     "If set at true, show the impact of each components and the value used for each " \
                                     "attribute \n " \
                                     "### 📋 Model name\n" \
                                     "You can have a list of available server models names [here](" \
                                     "#/server/server_get_all_archetype_name_v1_server_all_default_models_get)\n " \
                                     "\n### 🧮 Measure\n" \
                                     "The impacts is the sum of the components impacts"

server_impact_by_config_description = "# ✔️Server impacts from configuration\n" \
                                      "Retrieve the impacts of a given server configuration. Support manufacture *(" \
                                      "GWP, PE, ADP)* and usage *(GWP)* impacts.\n" \
                                      "### 💡 Smart complete\n" \
                                      "All missing data are retrieve with the closest available values. If no data are " \
                                      "available default maximizing data are used\n " \
                                      "### 👄 Verbose\n" \
                                      "If set at true, show the impact of each components and the value used for each " \
                                      "attribute \n " \
                                      "### 📋 Archetype\n" \
                                      "An archetype is a pre-registered server model. An ```archetype``` can be " \
                                      "specify in the model object. In case an archetype is specified, " \
                                      "all missing data are retrieve from the archetype. You can have a list of " \
                                      "available archetype's server models [here](" \
                                      "#/server/server_get_all_archetype_name_v1_server_all_default_models_get)\n " \
                                      "\n### 🧮 Measure\n" \
                                      "The impacts is the sum of the components impacts"

all_default_model_description = "# ✔️Get all the available server models\n" \
                                "Return the name of all pre-registered server models"

components_description = "### 💡 Smart complete\n" \
                         "All missing data are retrieve with the closest available values. If no data are " \
                         "available default maximizing data are used\n " \
                         "### 👄 Verbose\n" \
                         "If set at true, show the the values used for each attribute" \
                         "*Components have no units since they represent a single instance of a component.*"

default_calculation = "\n### 🧮 Measure\n" \
                      "The impacts values are set by default"

cpu_description = "# ✔️CPU impact from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = ( " \
                  "cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0," \
                  "491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "cpu<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> "

ssd_description = "# ✔️SSD impact from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>ssd<sub>manuf<sub><em>criteria</em></sub></sub> =  ( ssd<sub>size</sub> " \
                  "ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ssd<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> "

hdd_description = "# ✔️HDD impact from configuration\n" + components_description + default_calculation

ram_description = "# ✔️RAM impact from configuration\n" + components_description + \
                  "\n### 🧮 Measure\n" \
                  "<h3>ram<sub>manuf<sub><em>criteria</em></sub></sub> =( ram<sub>size</sub> " \
                  "/ ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + " \
                  "ram<sub>manuf_base<sub><em>criteria</em></sub></sub> </h3> "

motherboard_description = "# ✔️Motherboard impact from configuration\n" + components_description + default_calculation
power_supply_description = "# ✔️Power supply impact from configuration\n" + components_description + \
                           "\n### 🧮 Measure\n" + \
                           "<h3>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>unit<sub>weight</sub></sub>" \
                           " x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h3> "

case_description = "# ✔ Case impact from configuration\n" + components_description + default_calculation
