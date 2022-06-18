import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from boaviztapi import __version__

from boaviztapi.routers.component_router import component_router
from boaviztapi.routers.server_router import server_router
from boaviztapi.routers.cloud_router import cloud_router

from fastapi.responses import HTMLResponse

# Serverless frameworks adds a 'stage' prefix to the route used to serve applications
# We have to manage it to expose openapi doc on aws and generate proper links.
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(root_path=openapi_prefix)  # Here is the magic

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


@app.get("/", response_class=HTMLResponse)
async def welcom_page():
    html_content = """
    <html>
        <head>
            <title>BOAVIZTAPI</title>
        </head>
        <body>
            <p align="center">
                <img src="https://boavizta.org/media/site/d84925bc94-1642413712/boavizta-logo-4.png" width="100">
            </p>
            <h1 align="center">
              Welcome to BOAVIZTAPI
            </h1>
            <h2 align="center">
              Multicriteria & multistep impacts evaluations for digital assets
            </h2>
            </br>
            <h3 align="center">See our github repository : <a href="https://github.com/Boavizta/boaviztapi">LINK</a></h2>
            <h3 align="center">See OpenAPI specs (swagger) : <a href="docs">LINK</a></h2>
            <h3 align="center">See our complete documentation : <a href="https://doc.api.boavizta.org/">LINK</a></h2>
            <h3 align="center">See the other resources of Boavizta : <a href="https://boavizta.org/">LINK</a> </h2>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
