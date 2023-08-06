# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arg_services']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.32,<2.0', 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'arg-services',
    'version': '0.1.0',
    'description': 'GraphQL and gRPC schemas for Microservice-based Argumentation Machines.',
    'long_description': '# Argumentation Microservices\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
