import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from core.logging import InterceptHandler

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

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
