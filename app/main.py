import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request

from core.config import API_PREFIX, DEBUG, VERSION, WANDB_PROJECT_NAME
from core.events import preload_model_from_wandb
from core.logging import new_logger as logger
from services.prometheus import PrometheusMiddleware, metrics, setting_otlp

APP_NAME = os.environ.get("APP_NAME", "app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")


def get_application() -> FastAPI:
    application = FastAPI(title=WANDB_PROJECT_NAME,
                          debug=DEBUG, version=VERSION)
    # preload_model_from_wandb(application)
    application.add_event_handler(
        "startup", preload_model_from_wandb(application))
    application.logger = logger
    return application


app = get_application()

# Setting metrics middleware
logger.error(APP_NAME)
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@app.get('/custom-logger')
def customize_logger(request: Request):
    logger.info(APP_NAME)
    logger.info("Here Is Your Info Log")
    a = 1 / 0
    logger.error("Here Is Your Error Log")
    return {'data': "Successfully Implemented Custom Log"}
# @app.get("/chain")
# async def chain(response: Response):

#     headers = {}
#     inject(headers)  # inject trace info to header
#     logging.critical(headers)

#     async with httpx.AsyncClient() as client:
#         await client.get(f"http://localhost:8000/", headers=headers,)
#     async with httpx.AsyncClient() as client:
#         await client.get(f"http://{TARGET_ONE_HOST}:8000/io_task", headers=headers,)
#     async with httpx.AsyncClient() as client:
#         await client.get(f"http://{TARGET_TWO_HOST}:8000/cpu_task", headers=headers,)
#     logging.info("Chain Finished")
#     return {"path": "/chain"}


if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
