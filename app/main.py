import os

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
# from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException

from api.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, VERSION, WANDB_PROJECT_NAME
from core.events import preload_model_from_wandb


def get_application() -> FastAPI:
    application = FastAPI(title=WANDB_PROJECT_NAME,
                          debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    application.add_event_handler(
        "startup", preload_model_from_wandb(application))
    return application


app = get_application()
# Instrumentator().instrument(app).expose(app)

# TODO: Read port from environ?
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=8000, reload=False, debug=False)
