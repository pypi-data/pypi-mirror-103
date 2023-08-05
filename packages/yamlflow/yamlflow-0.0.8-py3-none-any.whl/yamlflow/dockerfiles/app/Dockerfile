ARG BACKEND

FROM ml_model_server:${BACKEND}

COPY model model

COPY service service

RUN pip install -r model/requirements.txt
