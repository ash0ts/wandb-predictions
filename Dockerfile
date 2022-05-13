FROM python:3.9.6

ENV PYTHONUNBUFFERED 1
ENV GROUP_ID=1000 \
    USER_ID=1000

# EXPOSE 8080
ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY Pipfile Pipfile.lock ./
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --system --deploy

COPY app ./

# Default env variables for imdb model. Can set and override from cloudbuild
ENV DEBUG=True
ENV WANDB_ENTITY="a-sh0ts"
ENV WANDB_PROJECT_NAME="kaggle-tps-mar-2022-odsc"
ENV MODEL_ARTIFACT_NAME="promoted_model"
ENV MODEL_ARTIFACT_VERSION="latest"

ENV PYTHONPATH app

CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
# CMD exec gunicorn --bind :${PORT:-5000} --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app
