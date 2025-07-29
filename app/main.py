import uvicorn
from app.router import api_router
from fastapi import FastAPI
from app.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, 
        version=settings.PROJECT_VERSION
    )
    app.include_router(api_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.API_APP_HOST, port=settings.API_APP_PORT)