import uvicorn
import logging
import logging.config
import app.jobs
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import api_router
from app.config import settings
from app.logging_config import LOGGING_CONFIG
from app.scheduler_config import scheduler

logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger("app")

def create_app(lifespan_rule) -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, 
        version=settings.PROJECT_VERSION,
        lifespan=lifespan_rule
    )
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = create_app(lifespan_rule = lifespan)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.API_APP_HOST, port=settings.API_APP_PORT, log_config=LOGGING_CONFIG)