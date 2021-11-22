import json


class Server:
    def __init__(self):
        self.brand = None
        self.name = None
        self.price = None
        self.weight = None
        self.height = None
        self.type = None

        self.cpu_number = None
        self.cpu_die = None
        self.cpu_core_number = None

        self.ram_capacity = None
        self.ram_strip_quantity = None
        self.ram_die = None

        self.hdd_number = None

        self.ssd_capacity = None
        self.ssd_quantity = None
        self.ssd_die = None

        self.power_supply_number = None
        self.power_supply_weight = None


def server_mapper(server_dto):
    # TODO: check consistency of the server_json and throw error
    server = Server()
    if server_dto.get("model") is not None:
        server.brand = server_dto.get("model").get("brand")
        server.name = server_dto.get("model").get("name")
        server.weight = server_dto.get("model").get("weight")
        server.height = server_dto.get("model").get("height")
        server.type = server_dto.get("model").get("type")

    if server_dto.get("configuration") is not None:
        if server_dto.get("configuration").get("cpu") is not None:
            server.cpu_number = server_dto.get("configuration").get("cpu").get("number")
            server.cpu_die = server_dto.get("configuration").get("cpu").get("die")
            server.cpu_core_number = server_dto.get("configuration").get("cpu").get("core_number")
        if server_dto.get("configuration").get("ram") is not None:
            server.ram_capacity = server_dto.get("configuration").get("ram").get("capacity")
            server.ram_strip_quantity = server_dto.get("configuration").get("ram").get("quantity")
            server.ram_die = server_dto.get("configuration").get("ram").get("die")
        if server_dto.get("configuration").get("hdd") is not None:
            server.hdd_number = server_dto.get("configuration").get("hdd").get("number")
        if server_dto.get("configuration").get("ssd") is not None:
            server.ssd_capacity = server_dto.get("configuration").get("ssd").get("capacity")
            server.ssd_quantity = server_dto.get("configuration").get("ssd").get("quantity")
            server.ssd_die = server_dto.get("configuration").get("ssd").get("die")

    return server
