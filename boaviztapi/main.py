from fastapi import FastAPI

from boaviztapi.routers.component_router import component_router
from boaviztapi.routers.server_router import server_router

app = FastAPI()

app.include_router(component_router)
app.include_router(server_router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=5000, reload=True, debug=True)
