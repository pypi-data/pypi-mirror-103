# yamlflow
Yet Another ML flow

## STATUS NOT READY

We follow `convention over configuration` (also known as coding by convention) software design paradigm.

Here are some of the features the `yamlflow` provides.


1. Build and publish your ML solution as a RESTful Web Service `with yaml`.
    
    + You don't need to write web realated code, or dockerfiles.
    
    + You don't need to benchmark which python web server or framework is best in terms of performance.
    
    + WE do it for you. All the best, packed in.


### Project structure 
```
.
├── models
│   ├── model_1
│   │   ├── api
│   │   │   └── model.py
│   │   └── data
│   │       ├── model.bin
│   │       └── model.xml
│   └── model_2
│       ├── api
│       │   └── model.py
│       └── data
│           └── model.pt
├── service
│   ├── data
│   ├── predictor.py
│   └── requirements.txt
├── train
│   ├── data
│   ├── requirements.txt
│   └── train.py
├── README.md
└── yamlflow.yaml
```

#### example `yamlflowflow.yaml`
```yaml
kind: Service
meta:
  project:
    name: ml-project
    version: 0.1.0
  registry: your.docker.registry
  user: dockerusername
backend:
  model_1:
    runtime: openvino
    device: cpu
  model_2:
    runtime: torch
    device: gpu
```


### example `predictor.py`
```py
 
```

### User guide
```bash
pip install yamlflow
yamlflow init
yamlflow build -f yamlflow.yaml
```

### Developer guide
```
pyenv install 3.8.6
poetry env use ~/.pyenv/versions/3.8.6/bin/python
poetry shell
poetry install
```

## TODO

+ build context
