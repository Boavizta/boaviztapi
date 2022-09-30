import json
import os

import markdown
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from boaviztapi import __version__

from boaviztapi.routers.component_router import component_router
from boaviztapi.routers.consumption_profile_router import consumption_profile
from boaviztapi.routers.server_router import server_router
from boaviztapi.routers.cloud_router import cloud_router
from boaviztapi.routers.utils_router import utils_router

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", [])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(server_router)
app.include_router(cloud_router)
app.include_router(component_router)
app.include_router(utils_router)
app.include_router(consumption_profile)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=5000, reload=True, debug=True)


@app.on_event("startup")
def my_schema():
    intro = open(os.path.join(os.path.dirname(__file__), 'routers/openapi_doc/intro_openapi.md'), 'r')
    openapi_schema = get_openapi(
        title="BOAVIZTAPI - DEMO",
        version=__version__,
        description=markdown.markdown(intro.read()),
        routes=app.routes,
        servers=app.servers,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
