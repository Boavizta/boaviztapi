from flask import Flask

from API.api.route.component_route import component_api
from API.api.route.server_route import server_api

app = Flask(__name__)

app.register_blueprint(server_api)
app.register_blueprint(component_api)


if __name__ == '__main__':
    app.run()
