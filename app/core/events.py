import os
from typing import Callable

from fastapi import FastAPI
from services.wandb import create_model

from core.config import API_PREFIX, IMAGE_PREDICTOR


def preload_model_from_wandb(app: FastAPI) -> Callable:

    def set_api():
        from api.routes.api import create_api_router
        model = create_model()
        app.include_router(create_api_router(
            model, IMAGE_PREDICTOR), prefix=API_PREFIX)

    return set_api
