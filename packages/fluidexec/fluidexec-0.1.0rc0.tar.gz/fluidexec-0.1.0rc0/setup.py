# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluid', 'workloads', 'workloads.common', 'workloads.word_language_model']

package_data = \
{'': ['*'], 'workloads.word_language_model': ['data/wikitext-2/README']}

install_requires = \
['numpy', 'ray[tune]==0.8.5', 'requests']

extras_require = \
{'exp': ['hpbandster', 'ConfigSpace', 'pandas']}

setup_kwargs = {
    'name': 'fluidexec',
    'version': '0.1.0rc0',
    'description': 'Resource-aware hyperparameter tuning execution engine',
    'long_description': '# Fluid: Resource-Aware Hyperparameter Tuning Engine\n\n[![PyPI version](https://img.shields.io/pypi/v/fluidexec.svg)](https://pypi.org/project/fluidexec)\n[![Build Status](https://github.com/SymbioticLab/fluid/actions/workflows/python-package/badge.svg?event=release)](https://github.com/SymbioticLab/fluid/actions)\n\n`Fluid` is an alternative [Ray](https://ray.io) executor that intelligently manages trial executions on behalf of hyperparameter tuning algorithms, in order to increase the resource utilization, and improve end-to-end makespan.\n\nThis is the implementation of our MLSys\'21 [paper](https://symbioticlab.org/publications/#/venue:MLSys) "Fluid: Resource-Aware Hyperparameter Tuning Engine".\n\n## Get Started\nFirst follow the [instruction](https://docs.ray.io/en/master/tune/index.html) in Ray Tune to setup the Ray cluster and a tuning environment as usual.\n\nThen make sure [Nvidia MPS](https://docs.nvidia.com/deploy/mps/index.html#topic_6_1) is correctly setup on all worker nodes.\n\n`Fluid` itself is a normal python package that can be installed by `pip install fluidexec`. Note that the pypi package name is `fluidexec` because the name `fluid` is already taken.\n\nTo use `Fluid` in Ray Tune, pass an instance of it as an additional keyword argument to `tune.run`:\n\n```python\nfrom fluid.executor import MyRayTrialExecutor\nfrom fluid.scheduler import FluidBandScheduler\ntune.run(\n    MyTrainable,\n    scheduler=FluidBandScheduler(...),\n    trial_executor=FluidExecutor(),\n    ...\n)\n```\n\n\n## Reproduce Experiments\nSee the README in [`workloads`](workloads/) for more information.\n\n\n## Notes\n\nPlease consider to cite our paper if you find this useful in your research project.\n\n```bibtex\n@inproceedings{fluid:mlsys21,\n    author    = {Peifeng Yu and Jiachen Liu and Mosharaf Chowdhury},\n    booktitle = {MLSys},\n    title     = {Fluid: Resource-Aware Hyperparameter Tuning Engine},\n    year      = {2021},\n}\n```\n',
    'author': 'Peifeng',
    'author_email': 'peifeng@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SymbioticLab/fluid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
