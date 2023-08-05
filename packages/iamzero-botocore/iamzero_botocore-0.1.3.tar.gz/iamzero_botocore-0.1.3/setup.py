# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iamzero_botocore']

package_data = \
{'': ['*']}

install_requires = \
['botocore>=1.20.54,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'iamzero-botocore',
    'version': '0.1.3',
    'description': 'iam-zero instrumentation for AWS botocore',
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
