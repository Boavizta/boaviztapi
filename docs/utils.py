from boaviztapi.model.device import DeviceServer
from boaviztapi.model.device.userTerminal import DeviceLaptop, DeviceDesktop, DeviceTablet, DeviceSmartphone, \
    DeviceTelevision, DeviceSmartWatch, DeviceBox, DeviceUsbStick, DeviceExternalSSD, DeviceExternalHDD, DeviceMonitor
from boaviztapi.model.impact import IMPACT_CRITERIAS

if __name__ == '__main__':
    type = False
    DEVICE = DeviceServer
    str = ""
    d_perso = DEVICE()

    if hasattr(d_perso, "type"):
        type = True
        d_perso.type.value = "perso"
        d_pro = DEVICE()
        d_pro.type.value = "pro"

    if type :
        str = str + f""

        str = str + f"## {d_perso.NAME.lower()}\n\n{d_perso.NAME.lower()} has two ```types```: ```pro``` and ```perso```.\n\n### Embedded impacts\n\n| Criteria | Unit | pro | perso |\n|----------|------|-------|------|\n"

        for i in IMPACT_CRITERIAS:
            try:
                str+=f"| {i.name} | {i.unit} | {d_pro.impact_other(i.name)[0]} | {d_perso.impact_other(i.name)[0]} |\n"
            except (AttributeError, NotImplementedError):
                pass
        str += "\n### Usage\n"
        str = str + f"\n#### Pro\n\n| Name                         | Unit                         | Default values (default;min;max) | Description                                  | Example |\n|------------------------------|------------------------------|---------------------------------|----------------------------------------------|---------|\n| years_life_time              | None                         |                                 | Lifespan of the element                      | {d_pro.usage.life_time.value};{d_pro.usage.life_time.min};{d_pro.usage.life_time.max}       |\n| hours_electrical_consumption | Watt/hour                    |            {d_pro.usage.hours_electrical_consumption.value};{d_pro.usage.hours_electrical_consumption.min};{d_pro.usage.hours_electrical_consumption.max}                    | Average electrical consumption per hour      | 1     |"
        str = str + f"\n\n#### Perso\n\n| Name                         | Unit                         | Default values (default;min;max) | Description                                  | Example |\n|------------------------------|------------------------------|---------------------------------|----------------------------------------------|---------|\n| years_life_time              | None                         |                                 | Lifespan of the element                      | {d_perso.usage.life_time.value};{d_perso.usage.life_time.min};{d_perso.usage.life_time.max}       |\n| hours_electrical_consumption | Watt/hour                    |            {d_perso.usage.hours_electrical_consumption.value};{d_perso.usage.hours_electrical_consumption.min};{d_perso.usage.hours_electrical_consumption.max}                    | Average electrical consumption per hour      | 1     |"
    else:
        str = str + f"## {d_perso.NAME.lower()}\n\n### Embedded impacts\n\n| Criteria | Unit | value |\n|----------|------|------|\n"

        for i in IMPACT_CRITERIAS:
            try:
                str += f"| {i.name} | {i.unit} | {d_perso.impact_other(i.name)[0]} |\n"
            except (AttributeError, NotImplementedError):
                pass
        str += "\n### Usage\n"
        str = str + f"| Name                         | Unit                         | Default values (default;min;max) | Description                                  | Example |\n|------------------------------|------------------------------|---------------------------------|----------------------------------------------|---------|\n| years_life_time              | None                         |                                 | Lifespan of the element                      | {d_perso.usage.life_time.value};{d_perso.usage.life_time.min};{d_perso.usage.life_time.max}       |\n| hours_electrical_consumption | Watt/hour                    |            {d_perso.usage.hours_electrical_consumption.value};{d_perso.usage.hours_electrical_consumption.min};{d_perso.usage.hours_electrical_consumption.max}                    | Average electrical consumption per hour      | 1     |"

    print(str)


if __name__ == '__main__':
    print("| Criteria | Implemented   | Source |\n|-----------------------------------------------------|---------|----------|")
    for crit in IMPACT_CRITERIAS:
        print(f"| {crit.name} | no | https://base-impacts.ademe.fr/documents/Negaoctet.zip |")
