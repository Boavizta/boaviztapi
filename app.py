from flask import Flask
from api.route.server_route import server_api

app = Flask(__name__)
app.register_blueprint(server_api)

if __name__ == '__main__':
    app.run()
