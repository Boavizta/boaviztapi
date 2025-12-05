import contextlib
import json
import logging
import os
import threading
import time
from typing import AsyncIterator

import anyio
import markdown
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from mangum import Mangum
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import Response

from boaviztapi.routers.portfolio_router import portfolio_router
from boaviztapi.routers.sustainability_router import sustainability_router
from boaviztapi.routers.user_router import user_router
from boaviztapi.service.carbon_intensity_provider import CarbonIntensityProvider
from boaviztapi.service.costs_provider import ElectricityCostsProvider
from boaviztapi.utils.auth_backend import JWTAuthBackend
from boaviztapi.utils.get_version import get_version_from_pyproject
from boaviztapi.application_context import get_app_context
from boaviztapi.routers.auth_router import auth_router
from boaviztapi.routers.cloud_router import cloud_router
from boaviztapi.routers.component_router import component_router
from boaviztapi.routers.configuration_router import configuration_router
from boaviztapi.routers.consumption_profile_router import consumption_profile
from boaviztapi.routers.electricity_prices_router import electricity_prices_router
from boaviztapi.routers.iot_router import iot
from boaviztapi.routers.options_router import options_router
from boaviztapi.routers.peripheral_router import peripheral_router
from boaviztapi.routers.server_router import server_router
from boaviztapi.routers.terminal_router import terminal_router
from boaviztapi.routers.utils_router import utils_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
_logger = logging.getLogger(__name__)

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # TODO: persist cache using postgres/redis, etc.
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")  # initialize in-memory cache

    _ctx = get_app_context()
    _ctx.load_secrets()
    await _ctx.create_db_connection()

    _logger.info("Starting caches...")
    electricity_prices_cache = ElectricityCostsProvider.get_cache_scheduler()
    carbon_intensity_cache = CarbonIntensityProvider.get_cache_scheduler()
    await electricity_prices_cache.startup()
    await carbon_intensity_cache.startup()

    yield
    await _ctx.close_db_connection()


# Serverless frameworks adds a 'stage' prefix to the route used to serve applications
# We have to manage it to expose openapi doc on aws and generate proper links.
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(lifespan=lifespan, root_path=openapi_prefix)  # Here is the magic
origins = json.loads(os.getenv("ALLOWED_ORIGINS", '["*"]'))
version = get_version_from_pyproject()
ctx = get_app_context()


# Ensure that even an uncaught exception includes CORS headers.
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # ignore anyio's EndOfStream exception traceback which just clutters up logs
        if isinstance(e.__context__, anyio.EndOfStream):
            e.__suppress_context__ = True

        _logger.exception(str(e), exc_info=e)
        return Response('Internal Server Error', status_code=500)

# app.add_middleware(AuthenticationMiddleware, backend=SessionAuthBackend())

# app.add_middleware(SessionMiddleware,
#                    secret_key=ctx.SESSION_MIDDLEWARE_SECRET_KEY,
#                    https_only=os.getenv("SESSION_MIDDLEWARE_HTTPS_ONLY", False),
#                    max_age=os.getenv("SESSION_MIDDLEWARE_MAX_AGE", 3600))

app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


app.middleware('http')(catch_exceptions_middleware)

app.include_router(server_router)
app.include_router(cloud_router)
app.include_router(terminal_router)
app.include_router(peripheral_router)
app.include_router(component_router)
app.include_router(iot)
app.include_router(consumption_profile)
app.include_router(utils_router)
app.include_router(electricity_prices_router)
app.include_router(options_router)
app.include_router(configuration_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(portfolio_router)
app.include_router(sustainability_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=5000, reload=True)


@app.on_event("startup")
def my_schema():
    intro = open(os.path.join(os.path.dirname(__file__), 'routers/openapi_doc/intro_openapi.md'), 'r', encoding='utf-8')
    openapi_schema = get_openapi(
        title="BOAVIZTAPI - DEMO",
        version=version,
        description=markdown.markdown(intro.read()),
        routes=app.routes,
        servers=app.servers,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema


# Wrapper for aws/lambda serverless app
handler = Mangum(app)


@app.get("/", response_class=HTMLResponse)
async def welcome_page():
    html_content = """
    <html>
        <head>
            <title>BOAVIZTAPI</title>
            <style>
                * {
                    font-family: sans-serif;
                }
            </style>
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
            %s
        </body>
    </html>
    """ % os.getenv('SPECIAL_MESSAGE', '')
    return HTMLResponse(content=html_content, status_code=200)


# # A uvicorn server that can be run in a thread. Taken from @florimondmanca @
# https://github.com/encode/uvicorn/issues/742#issuecomment-674411676
class UvicornServerThreaded(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
