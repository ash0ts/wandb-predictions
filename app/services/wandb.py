import os
from pathlib import Path

from core.config import (MODEL_ARTIFACT_NAME, MODEL_ARTIFACT_VERSION,
                         WANDB_ENTITY, WANDB_PROJECT_NAME)
from core.utils import logging_wrap
from loguru import logger

import wandb


class WANDB_MODEL(object):

    def __init__(self):

        self.model_art_path = None
        self.deployment_artifacts_path = None
        self.model_path = None

        self.model = None
        self.deployment = None

        self.load_model = None
        self.predict = None

        self.Request = None
        self.Response = None

    def download_latest_model(self):

        # TODO: pass information about the download operation here
        wandb_art_path = str(Path(WANDB_ENTITY, WANDB_PROJECT_NAME,
                                  MODEL_ARTIFACT_NAME, MODEL_ARTIFACT_VERSION))
        run = wandb.init(project=WANDB_PROJECT_NAME,
                         name="download-model", job_type="deployment")
        wandb_art_path = f"{WANDB_ENTITY}/{WANDB_PROJECT_NAME}/{MODEL_ARTIFACT_NAME}:{MODEL_ARTIFACT_VERSION}"
        model_art = run.use_artifact(wandb_art_path)
        model_art_path = self.model_art_path = model_art.download()

        self.deployment_artifacts_path = os.path.join(
            model_art_path, "deployment")
        self.model_path = os.path.join(model_art_path, 'promoted_model')

        run.finish()
        return None

    # (2)
    def install(self):
        import os
        import subprocess
        import sys
        command = [
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            os.path.join(self.deployment_artifacts_path, 'requirements.txt'),
            '--no-cache-dir'
        ]

        subprocess.check_call(command)

    # (3)
    def set_deployment_code(self):
        from importlib.machinery import SourceFileLoader

        # imports the module from the given path
        deployment = self.deployment = SourceFileLoader("predict", os.path.join(
            self.deployment_artifacts_path, "predict.py")).load_module()

        # self.load_wandb_model = logging_wrap(deployment.load_wandb_model)
        # self.predict = logging_wrap(deployment.predict)

        self.load_wandb_model = deployment.load_wandb_model
        self.predict = deployment.predict

        self.Request = deployment.Request
        self.Response = deployment.Response

        return None

    # (4)
    def set_model(self):
        self.model = self.load_wandb_model(self.model_path)


def create_model():
    model = WANDB_MODEL()
    model.download_latest_model()
    model.install()
    model.set_deployment_code()
    model.set_model()
    return model
