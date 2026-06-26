server_impact_by_model_description = (
    "# ✔ ️Server impacts from model name\n"
    "Retrieve the impacts of a given server archetype.\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "🔌 Usage\n\n"
    "📋 Archetype: "
    "Uses the classic server impacts router with a pre-registered archetype \n\n"
    "⏬ Allocation"
)

server_impact_by_config_description = (
    "# ✔️ Server impacts from configuration\n"
    "Retrieve the impacts of a given server configuration.\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "* 📈 Modeled\n\n"
    "📋 Archetype\n\n"
    "⏬ Allocation"
)

all_archetype_servers = "# ✔️ Get all the available server archetype\n"
all_archetype_components = (
    "# ✔️ Get all the available component archetype for a given component name\n"
)
all_archetype_user_terminals = (
    "# ✔️ Get all the available user terminal archetype for a given user terminal name\n"
)
all_terminal_categories = "# ✔️ Get all the available user terminal router\n"
all_peripheral_categories = "# ✔️ Get all the available user peripheral router\n"
all_user_terminal_subcategories = (
    "# ✔️ Get all the available user terminal subcategories\n"
)
all_default_usage_values = "# ✔️ Get all default usage values for a given user terminal category and subcategory\n"

get_archetype_config_desc = "# ✔️ Get the configuration of a given archetype\n"
get_instance_config = (
    "# ✔️ Get the configuration of a given instance\n"
    "Returns the archetype configuration for the requested instance. "
    "Fuzzy matching is applied if the exact name is not found — see the instance impact endpoint for details.\n"
)

cpu_description = (
    "# ✔ ️CPU impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "<h3>cpu<sub>manuf<sub><em>criteria</em></sub></sub> = ( "
    "cpu<sub>core<sub>units</sub></sub> x cpu<sub>diesize</sub> + 0,"
    "491 ) x cpu<sub>manuf_die<sub><em>criteria</em></sub></sub> + "
    "cpu<sub>manuf_base<sub><em>criteria</em></sub></sub></h3> "
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "* 📈 Modeled\n\n"
    "⏬ Allocation"
)

gpu_description = (
    "# ✔ ️GPU impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "<h3>gpu<sub>manuf<sub><em>criteria</em></sub></sub> = "
    "gpu<sub>casing_weight</sub> x gpu<sub>manuf_casing<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>heatsink_weight</sub> x gpu<sub>manuf_heatsink<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>pwb_surface</sub> x gpu<sub>manuf_pwb<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>surface</sub> x gpu<sub>manuf_gpu_die<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>vram_surface</sub> x gpu<sub>manuf_vram_die<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>transport_distance_boat</sub> x gpu<sub>impact_boat<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>transport_distance_truck</sub> x gpu<sub>impact_truck<sub><em>criteria</em></sub></sub> + "
    "gpu<sub>transport_distance_plane</sub> x gpu<sub>impact_plane<sub><em>criteria</em></sub></sub></h3> "
    "🔌 Usage\n\n"
    "* ❌ Not implemented\n\n"
    "⏬ Allocation"
)

ssd_description = (
    "# ✔ ️SSD impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "<h3>ssd<sub>manuf<sub><em>criteria</em></sub></sub> =  ( ssd<sub>size</sub> "
    "ssd<sub>density</sub> ) x ssd<sub>manuf_die<sub><em>criteria</em></sub></sub> + "
    "ssd<sub>manuf_base<sub><em>criteria</em></sub></sub></h3>"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "⏬ Allocation"
)

hdd_description = (
    "# ✔ ️HDD impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "The impacts values are set by default"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "⏬ Allocation"
)

ram_description = (
    "# ✔️ RAM impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "<h3>ram<sub>manuf<sub><em>criteria</em></sub></sub> =( ram<sub>size</sub> "
    "/ ram<sub>density</sub> ) x ram<sub>manuf_die<sub><em>criteria</em></sub></sub> + "
    "ram<sub>manuf_base<sub><em>criteria</em></sub></sub> </h3> "
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "* 📈 Modeled\n\n"
    "⏬ Allocation"
)

motherboard_description = (
    "# ✔ ️Motherboard impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "The impacts values are set by default"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "⏬ Allocation"
)

power_supply_description = (
    "# ✔ ️Power supply impacts from configuration\n" + "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "<h3>psu<sub>manuf<sub><em>criteria</em></sub></sub> = psu<sub>unit<sub>weight</sub></sub>"
    " x psu<sub>manuf_weight<sub><em>criteria</em></sub></sub></h3> "
    "🔌 Usage\n\n"
    "* ⏺️  Given : shouldn't be used\n\n"
    "⏬ Allocation"
)

case_description = (
    "# ✔ ️Case impacts from configuration\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "🔌 Usage\n\n"
    "* ⏺️  Given : when the enclosure consumes energy \n\n"
    "⏬ Allocation"
)

cloud_provider_description = (
    "# ✔ ️Cloud instance impacts from provider, instance type and usage \n"
    "Retrieve the impacts of a given Cloud instance and usage.\n\n"
    "### Features\n\n"
    "📋 Provider \n\n"
    "Name of the cloud provider. You can retrieve the [list here]("
    "#/cloud_instance/server_get_all_cloud_providers).\n\n"
    "📋 Instance type \n\n"
    "Name of the chosen instance. You can retrieve the [list here]("
    "#/cloud/server_get_archetype_name_v1_cloud_all_aws_instances_get).\n\n"
    "🔍 Fuzzy matching \n\n"
    "If the instance type is not found exactly, the API applies a staged fuzzy-matching "
    "algorithm to resolve near-miss names:\n\n"
    "1. **Normalization** — all separator and capitalisation variants are tested in "
    "parallel (`Standard_D2ads_v5`, `D2ads-v5`, `d2ads v5` all resolve to `d2ads_v5`).\n\n"
    "2. **Hamming distance** — single-character substitutions on equal-length names.\n\n"
    "3. **Levenshtein distance** — insertions / deletions for differing-length names.\n\n"
    "When a substitution occurs, the response includes a top-level `warnings` field "
    "identifying the matched instance.\n\n"
    "👄 Verbose\n\n"
    "🔨 Embedded\n\n"
    "🔌 Usage \n\n"
    "* 📈 Modeled\n\n"
    "📋 Archetype : The configuration is set by the API, only usage is given by the user\n\n"
    "⏬ Allocation"
)

all_default_cloud_instances = (
    "# ✔ ️Get all the available instances for a given Cloud provider\n"
    "📜 Return the name of all pre-registered instances for the Cloud provider"
)

all_default_cloud_providers = (
    "# ✔ ️Get all the available Cloud providers\n"
    "📜 Return the names of all pre-registered Cloud providers"
)

country_code = "# ✔ ️Get all the available countries with their trigram code (*usage:{usage_location: 'FRA'}*)\n"
cloud_regions = (
    "# ✔ ️Get all available cloud regions\n"
    "📜 Return the list of available cloud regions for each provider, optionally filtered by a specific provider.\n"
    "Can be used in cloud instance requests with *usage:{region: 'eu-west-3'}*"
)
cpu_family = (
    "# ✔ ️Get all the available cpu family in the API (*cpu:{family:'skylake'}*)\n"
)
cpu_model_range = "# ✔ ️Get all the available cpu family in the API (*cpu:{model_range:'xeon platinum'}*)\n"
ssd_manufacturer = "# ✔ ️Get all the available ssd manufacturer in the API (*ssd:{manufacturer:'samsung'}*)\n"
ram_manufacturer = "# ✔ ️Get all the available ram manufacturer in the API (*ram:{manufacturer:'samsung'}*)\n"
case_type = "# ✔ ️Get all the available case type in the API (*model:{case:'blade'}*)\n"
name_to_cpu = "# ✔ ️Complete a cpu attributes from a cpu name\n"
cpu_names = "# ✔ ️Get all the available cpu name in the API (*cpu:{name:'intel xeon platinum 8175m'}*)\n"
name_to_gpu = "# ✔ ️Complete a gpu attributes from a gpu name\n"
gpu_names = "# ✔ ️Get all the available gpu name in the API (*gpu:{name:'nvidia a100 80gb sxm'}*)\n"
impacts_criteria = "# ✔ ️Get all the available criteria for the impacts calculation\n"


terminal_description = (
    "# ✔ Terminal impacts\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "The impacts values are fix"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "* 📋 Archetype\n\n"
    "⏬ Allocation"
)


peripheral_description = (
    "# ✔ Peripheral impacts\n"
    "### Features\n\n"
    "👄 Verbose\n\n"
    "🔃 Auto-complete\n\n"
    "🔨 Embedded\n\n"
    "The impacts values are fix"
    "🔌 Usage\n\n"
    "* ⏺️  Given\n\n"
    "* 📋 Archetype\n\n"
    "⏬ Allocation"
)
