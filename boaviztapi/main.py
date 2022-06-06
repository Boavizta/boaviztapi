import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from boaviztapi import __version__

from boaviztapi.routers.component_router import component_router
from boaviztapi.routers.server_router import server_router
from boaviztapi.routers.cloud_router import cloud_router

# Serverless frameworks adds a 'stage' prefix to the route used to serve applications
# We have to manage it to expose openapi doc on aws.
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(openapi_prefix=openapi_prefix) # Here is the magic
# app = FastAPI()

app.include_router(server_router)
app.include_router(cloud_router)
app.include_router(component_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=5000, reload=True, debug=True)



@app.on_event("startup")
def my_schema():
    openapi_schema = get_openapi(
        title="BOAVIZTAPI - DEMO",
        version=__version__,
        description="# 🎯 Retrieving the impacts of digital elements\n"
                    "This is a quick demo, to see full documentation [click here](https://doc.api.boavizta.org) \n"
                    "## ➡️Server router \n"
                    "### Server routers support the following impacts: \n"
                    "| Impact | 🔨 Manufacture | 🔌 Usage |\n"
                    "|--------|----------------|----------|\n"
                    "|   GWP  |        X       |     X    |\n"
                    "|   ADP  |        X       |     X    |\n"
                    "|   PE   |        X       |     X    |\n"
                    "## ➡️Cloud router \n"
                    "### Cloud routers support the following impacts: \n"
                    "| Impact | 🔨 Manufacture | 🔌 Usage |\n"
                    "|--------|----------------|----------|\n"
                    "|   GWP  |        X       |     X    |\n"
                    "|   ADP  |        X       |     X    |\n"
                    "|   PE   |        X       |     X    |\n"
                    "## ➡️Component router \n"
                    "### Component routers support the following impacts: \n"
                    "| Impact | 🔨 Manufacture | 🔌 Usage |\n"
                    "|--------|----------------|----------|\n"
                    "|   GWP  |        X       |          |\n"
                    "|   ADP  |        X       |          |\n"
                    "|   PE   |        X       |          |\n",
        routes=app.routes,
        servers=app.servers,
    )
    app.openapi_schema = openapi_schema
    
    return app.openapi_schema

# Wrapper for aws/lambda serverless app
handler = Mangum(app)
