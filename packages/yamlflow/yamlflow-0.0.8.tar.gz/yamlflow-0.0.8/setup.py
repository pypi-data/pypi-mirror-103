# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlflow',
 'yamlflow.cli',
 'yamlflow.cli.commands',
 'yamlflow.dockerfiles.core.scripts']

package_data = \
{'': ['*'],
 'yamlflow': ['dockerfiles/app/*',
              'dockerfiles/backend/sklearn-cpu/*',
              'dockerfiles/backend/torch-cpu/*',
              'dockerfiles/core/*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'docker>=5.0.0,<6.0.0', 'pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['yamlflow = yamlflow.cli:main']}

setup_kwargs = {
    'name': 'yamlflow',
    'version': '0.0.8',
    'description': 'Yet Another ML flow',
    'long_description': "# yamlflow\nYet Another ML flow\n\n## STATUS NOT READY\n\nWe follow `convention over configuration` (also known as coding by convention) software design paradigm.\n\nHere are some of the features the `yamlflow` provides.\n\n\n1. Build and publish your ML solution as a RESTful Web Service `with yaml`.\n    \n    + You don't need to write web realated code, or dockerfiles.\n    \n    + You don't need to benchmark which python web server or framework is best in terms of performance.\n    \n    + WE do it for you. All the best, packed in.\n\n\n### Project structure \n```\n.\n├── models\n│   ├── model_1\n│   │   ├── api\n│   │   │   └── model.py\n│   │   └── data\n│   │       ├── model.bin\n│   │       └── model.xml\n│   └── model_2\n│       ├── api\n│       │   └── model.py\n│       └── data\n│           └── model.pt\n├── service\n│   ├── data\n│   ├── predictor.py\n│   └── requirements.txt\n├── train\n│   ├── data\n│   ├── requirements.txt\n│   └── train.py\n├── README.md\n└── yamlflow.yaml\n```\n\n#### example `yamlflowflow.yaml`\n```yaml\nkind: Service\nmeta:\n  project:\n    name: ml-project\n    version: 0.1.0\n  registry: your.docker.registry\n  user: dockerusername\nbackend:\n  model_1:\n    runtime: openvino\n    device: cpu\n  model_2:\n    runtime: torch\n    device: gpu\n```\n\n\n### example `predictor.py`\n```py\n \n```\n\n### User guide\n```bash\npip install yamlflow\nyamlflow init\nyamlflow build -f yamlflow.yaml\n```\n\n### Developer guide\n```\npyenv install 3.8.6\npoetry env use ~/.pyenv/versions/3.8.6/bin/python\npoetry shell\npoetry install\n```\n\n## TODO\n\n+ build context\n",
    'author': 'Sevak Harutyunyan',
    'author_email': 'sevak.g.harutyunyan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sevakharutyunyan/aida',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
