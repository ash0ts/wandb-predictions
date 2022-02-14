from typing import Callable

from fastapi import FastAPI
from services.wandb import WANDB_MODEL


def preload_model_from_wandb(app: FastAPI) -> Callable:
    def model_app() -> None:
        WANDB_MODEL.download_latest_model()
        WANDB_MODEL.install()
        WANDB_MODEL.set_deployment_code()
        WANDB_MODEL.set_model()

    return model_app
