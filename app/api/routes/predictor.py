from typing import Any

from core.errors import PredictException
from fastapi import APIRouter, HTTPException
from loguru import logger
from models.prediction import HealthResponse


def create_prediction_router(model) -> APIRouter:
    # from services.wandb import WANDB_MODEL as model

    router = APIRouter()

    # TODO: Let the passed logged model script define the model response? Or expect generic response and let model process output
    logger.info(model.Response)
    logger.info(model.Request)

    @router.get("/predict", name="predict:get-data", response_model=model.Response)
    # async def predict(request: BERTSentimentRequest):
    async def predict(request: model.Request):
        # text = request.text
        request_dict = request.dict()
        # if not request:
        if not request:
            raise HTTPException(
                status_code=404, detail="'data_input' argument invalid!")
        try:
            # TODO: Fix this mess of a prediction flow. Make it so I don't need to pass the model? Or overwrite the class somehow as we expect a logged
            # predict code to always pass a model first and then inputs after?
            prediction = model.predict(model.model, request_dict)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Exception: {e}")

        return prediction

    @router.get(
        "/health", response_model=HealthResponse, name="health:get-data",
    )
    async def health():
        is_health = False
        try:
            # TODO: Run test in health check
            # test_text = [
            #     'This was an awesome movie. I watch it twice my time watching this beautiful movie if I have known it was this good']
            # print(test_text)
            # model.predict(test_text)
            is_health = True
            return HealthResponse(status=is_health)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Unhealthy")

    return router
