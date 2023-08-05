import os
import sys
from dataclasses import dataclass, asdict

import yaml

from yamlflow.cli.constants import BASE_DIR


@dataclass(frozen=True, order=True)
class _meta:
    registry: str
    user: str

    def __repr__(self):
        return f"{self.registry}/{self.user}"


@dataclass(frozen=True, order=True)
class _project:
    name: str
    version: str

    def __repr__(self):
        return f"{self.name}:{self.version}"


@dataclass(frozen=True, order=True)
class _backend:
    runtime: str
    device: str
    
    def __repr__(self):
        return f"{self.runtime}-{self.device}"



class Manifest:

    def __init__(self, mainfest_path: str):
        super().__init__()
        with open(mainfest_path, 'r') as fp:
            try:
                self._data = yaml.safe_load(fp)
            except yaml.YAMLError as err:
                print(err)
                sys.exit(1)
        self._meta = self._data["meta"]
        self._project = self._data["project"]
        self._backend = self._data["backend"]
        

    @property
    def meta(self):
        return repr(_meta(**self._meta))

    
    @property
    def project(self):
        return repr(_project(**self._project))


    @property
    def backend(self):
        return repr(_backend(**self._backend))


    def build_info(self):
        return {
            "path": BASE_DIR,
            "tag": f"{self.meta}/{self.project}",
            "buildargs": {"BACKEND": self.backend}
        }
