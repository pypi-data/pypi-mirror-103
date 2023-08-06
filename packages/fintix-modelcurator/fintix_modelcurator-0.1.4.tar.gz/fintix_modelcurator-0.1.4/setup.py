# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fintix_modelcurator']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'confluent-kafka>=1.6.1,<2.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'pandas>=1.2.4,<2.0.0',
 'plotly==4.14.3',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'tensorflow-io>=0.17.1,<0.18.0',
 'tensorflow>=2.4.1,<3.0.0',
 'xgboost==1.4.1']

setup_kwargs = {
    'name': 'fintix-modelcurator',
    'version': '0.1.4',
    'description': 'helpers library used for model lab and model training and model deploying',
    'long_description': None,
    'author': 'Trinh Tran',
    'author_email': 'trinhtran2151995@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
