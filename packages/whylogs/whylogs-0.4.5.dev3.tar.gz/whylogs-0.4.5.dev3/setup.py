# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['whylogs',
 'whylogs.app',
 'whylogs.cli',
 'whylogs.core',
 'whylogs.core.metrics',
 'whylogs.core.statistics',
 'whylogs.core.statistics.datatypes',
 'whylogs.core.types',
 'whylogs.features',
 'whylogs.io',
 'whylogs.logs',
 'whylogs.mlflow',
 'whylogs.proto',
 'whylogs.util',
 'whylogs.viz',
 'whylogs.viz.matplotlib',
 'whylogs.whylabs_client']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.1',
 'botocore>=1.17.44',
 'click>=7.1.2',
 'fastparquet>=0.5.0,<0.6.0',
 'llvmlite>=0.36.0,<0.37.0',
 'marshmallow>=3.7.1',
 'matplotlib==3.3.3',
 'mlflow==1.13.1',
 'numpy==1.19.3',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.0.0',
 'protobuf>=3.15.5',
 'puremagic',
 'pyarrow>=3.0.0,<4.0.0',
 'python-dateutil>=2.8.1',
 'pyyaml>=5.3.1',
 'sklearn>=0.0,<0.1',
 'smart-open>=4.1.2',
 'tqdm>=4.60.0,<5.0.0',
 'whylabs-client',
 'whylabs-datasketches>=2.2.0b1',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'whylogs',
    'version': '0.4.5.dev3',
    'description': 'Profile and monitor your ML data pipeline end-to-end',
    'long_description': None,
    'author': 'WhyLabs.ai',
    'author_email': 'support@whylabs.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
