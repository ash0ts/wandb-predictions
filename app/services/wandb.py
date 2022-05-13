import os
from pathlib import Path

from core.config import (MODEL_ARTIFACT_NAME, MODEL_ARTIFACT_VERSION,
                         WANDB_ENTITY, WANDB_PROJECT_NAME)
from loguru import logger

import wandb


class WANDB_MODEL(object):

    model_art_path = None
    deployment_artifacts_path = None
    model_path = None

    model = None
    deployment = None

    load_model = None
    predict = None

    Request = None
    Response = None

    # (1)
    @classmethod
    def download_latest_model(cls):

        # TODO: pass information about the download operation here
        wandb_art_path = str(Path(WANDB_ENTITY, WANDB_PROJECT_NAME,
                                  MODEL_ARTIFACT_NAME, MODEL_ARTIFACT_VERSION))
        run = wandb.init(project=WANDB_PROJECT_NAME,
                         name="download-model", job_type="deployment")
        wandb_art_path = f"{WANDB_ENTITY}/{WANDB_PROJECT_NAME}/{MODEL_ARTIFACT_NAME}:{MODEL_ARTIFACT_VERSION}"
        logger.info(wandb_art_path)
        model_art = run.use_artifact(wandb_art_path)
        model_art_path = cls.model_art_path = model_art.download()
        logger.info(cls.model_art_path)
        logger.info(os.path.exists(cls.model_art_path))
        cls.deployment_artifacts_path = os.path.join(
            model_art_path, "deployment")
        cls.model_path = os.path.join(model_art_path, 'promoted_model')
        logger.info(cls.model_path)
        logger.info(os.path.exists(cls.model_path))

        logger.info(os.path.join(cls.model_path, "model.pkl"))
        logger.info(os.path.exists(os.path.join(cls.model_path, "model.pkl")))
        run.finish()
        return None

    # (2)
    @classmethod
    def install(cls):
        import os
        import subprocess
        import sys
        command = [
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            os.path.join(cls.deployment_artifacts_path, 'requirements.txt'),
            '--no-cache-dir'
        ]

        subprocess.check_call(command)

    # (3)
    @classmethod
    def set_deployment_code(cls):
        from importlib.machinery import SourceFileLoader

        # imports the module from the given path
        deployment = cls.deployment = SourceFileLoader("predict", os.path.join(
            cls.deployment_artifacts_path, "predict.py")).load_module()

        cls.load_wandb_model = deployment.load_wandb_model
        cls.predict = deployment.predict

        cls.Request = deployment.Request
        cls.Response = deployment.Response

        return None

    # (4)
    @classmethod
    def set_model(cls):
        cls.model = cls.load_wandb_model(cls.model_path)


def create_model():
    model = WANDB_MODEL()
    model.download_latest_model()
    model.install()
    model.set_deployment_code()
    model.set_model()
    return model
