import json


@property
class Server:
    def __init__(self):
        self.brand = None
        self.name = None
        self.price = None
        self.weight = None
        self.height = None
        self.type = None

        self.cpu_number = None
        self.cpu_type = None
        self.cpu_die = None

        self.ram_capacity = None
        self.ram_strip_model = None
        self.ram_strip_quantity = None
        self.ram_die = None

        self.hdd_number = None

        self.ssd_capacity = None
        self.ssd_model = None
        self.ssd_quantity = None
        self.ssd_die = None

        self.power_supply_number = None
        self.power_supply_weight = None


def server_mapper(server_json):
    # TODO: check consistency of the server_json and throw error
    server_dto = json.load(server_json)
    server = Server()

    server.brand = server_dto.get("mode").get("brand")
    server.name = server_dto.get("mode").get("name")
    server.weight = server_dto.get("mode").get("weight")
    server.height = server_dto.get("mode").get("height")
    server.type = server_dto.get("mode").get("type")

    server.cpu_number = server_dto.get("configuration").get("cpu").get("number")
    server.cpu_type = server_dto.get("configuration").get("cpu").get("type")
    server.cpu_die = server_dto.get("configuration").get("cpu").get("die")

    server.ram_capacity = server_dto.get("configuration").get("ram").get("capacity")
    server.ram_strip_model = server_dto.get("configuration").get("ram").get("model")
    server.ram_strip_quantity = server_dto.get("configuration").get("ram").get("quantity")
    server.ram_die = server_dto.get("configuration").get("ram").get("die")

    server.hdd_number = server_dto.get("configuration").get("hdd").get("number")

    server.ssd_capacity = server_dto.get("configuration").get("ssd").get("capacity")
    server.ssd_model = server_dto.get("configuration").get("ssd").get("model")
    server.ssd_quantity = server_dto.get("configuration").get("ssd").get("quantity")
    server.ssd_die = server_dto.get("configuration").get("ssd").get("die")

