# from typing import Any, List

# from core.errors import PredictException

from core.logging import new_logger as logger
from fastapi import APIRouter, File, HTTPException, UploadFile
from models.prediction import HealthResponse
from services.image_upload import read_imagefile


# TODO: Use type dispatch to ensure the response is well formed for FastAPI and the provided model response
def create_prediction_router(model, image_predictor=False) -> APIRouter:
    # from services.wandb import WANDB_MODEL as model

    router = APIRouter()

    # TODO: Let the passed logged model script define the model response? Or expect generic response and let model process output
    logger.info(model.Response)
    logger.info(model.Request)

    if image_predictor:
        @router.post("/predict", name="predict:make-prediction", response_model=model.Response)
        async def predict(file: UploadFile = File(...)):
            extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
            if not file:
                raise HTTPException(
                    status_code=404, detail="file not uploaded")
            elif not extension:
                raise HTTPException(
                    status_code=404, detail="invalid format of image upload")
            try:
                # TODO: Fix this mess of a prediction flow. Make it so I don't need to pass the model? Or overwrite the class somehow as we expect a logged
                # predict code to always pass a model first and then inputs after?
                image = read_imagefile(await file.read())
                prediction = model.predict(model.model, image)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Exception: {e}")

            return prediction

    else:
        @router.post("/predict", name="predict:make-prediction", response_model=model.Response)
        # async def predict(request: BERTSentimentRequest):
        async def predict(request: model.Request):
            # text = request.text
            logger.info(request)
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
