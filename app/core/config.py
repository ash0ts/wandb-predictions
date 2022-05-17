from starlette.config import Config

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT: int = config(
    "MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config(
    "MIN_CONNECTIONS_COUNT", cast=int, default=10)

WANDB_ENTITY = config("WANDB_ENTITY")
WANDB_PROJECT_NAME = config("WANDB_PROJECT_NAME")
MODEL_ARTIFACT_NAME = config("MODEL_ARTIFACT_NAME")
MODEL_ARTIFACT_VERSION = config("MODEL_ARTIFACT_VERSION")

IMAGE_PREDICTOR = config("IMAGE_PREDICTOR", cast=bool, default=False)
