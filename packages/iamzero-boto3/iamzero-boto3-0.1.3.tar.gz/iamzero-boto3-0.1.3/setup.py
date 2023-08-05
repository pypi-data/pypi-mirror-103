# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iamzero_boto3']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.54,<2.0.0', 'iamzero-botocore>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'iamzero-boto3',
    'version': '0.1.3',
    'description': 'The AWS SDK for Python, instrumented with iam-zero',
    'long_description': None,
    'author': 'Chris Norman',
    'author_email': 'chris@exponentlabs.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
