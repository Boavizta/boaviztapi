from marshmallow import Schema, fields


@property
class Server:
    def __init__(self, description, components):
        self.components = components
        self.description = description
        super().__init__()
