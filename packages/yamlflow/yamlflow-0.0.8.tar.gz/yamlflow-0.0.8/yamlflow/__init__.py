import os
from collections import namedtuple 

__version__ = '0.0.8'

here = os.path.abspath(os.path.dirname(__file__))

DockerImage = namedtuple("DockerImage", ["path", "tag"])

APP_DOCKERFILE = os.path.join(here, "dockerfiles", "app")

dockerfiles = (
    DockerImage(path=os.path.join(here, "dockerfiles", "core"), tag="ml_model_server:core"),
    DockerImage(path=os.path.join(here, "dockerfiles", "backend", "torch-cpu"), tag="ml_model_server:torch-cpu")
)
