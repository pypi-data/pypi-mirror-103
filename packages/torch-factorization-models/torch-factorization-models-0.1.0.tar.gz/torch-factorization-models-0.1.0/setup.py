# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_factorization_models']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pytorch-lightning>=0.9.0,<0.10.0',
 'ranking-metrics-torch>=0.3.0,<0.4.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'torch>=1.6.0,<2.0.0',
 'torch_optim_sparse>=0.1.2,<0.2.0',
 'wandb>=0.10.4,<0.11.0']

setup_kwargs = {
    'name': 'torch-factorization-models',
    'version': '0.1.0',
    'description': 'Factorization-based models for recommender systems',
    'long_description': None,
    'author': 'Karl Higley',
    'author_email': 'kmhigley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
