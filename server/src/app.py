from fastapi import FastAPI, Request
from src.container import AppContainer
from src import routers
import logging
from fastapi.responses import JSONResponse
from src.exceptions import ClientException, ServerException
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    container = AppContainer()

    app = FastAPI()
    app.container = container
    app.include_router(routers.router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )
    
    @app.exception_handler(ClientException)
    async def client_exception_handler(request: Request, exc: ClientException):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message, "code": exc.__class__.__name__},
        )
        
    @app.exception_handler(ServerException)
    async def server_exception_handler(request: Request, exc: ServerException):
        return JSONResponse(
            status_code=500,
            content={"message": exc.message, "code": exc.__class__.__name__},
        )
    
    @app.exception_handler(Exception)
    async def default_exception_handler(request: Request, exc: Exception):
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "서버에 에러가 발생했습니다.", "code": exc.__class__.__name__},
        )

    return app

app = create_app()