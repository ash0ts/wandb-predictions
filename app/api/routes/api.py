from fastapi import APIRouter

from api.routes import predictor


# TODO: REmove hard coding of model parameter
def create_api_router(model, image_predictor=False) -> APIRouter:
    router = APIRouter()
    router.include_router(predictor.create_prediction_router(model, image_predictor), tags=[
                          "predictor"], prefix="/v1")
    return router
