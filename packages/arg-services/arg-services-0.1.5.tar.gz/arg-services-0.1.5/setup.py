# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arg_services', 'arg_services_helper']

package_data = \
{'': ['*'],
 'arg_services': ['base/v1/base_pb2.pyi',
                  'base/v1/base_pb2.pyi',
                  'base/v1/base_pb2_grpc.pyi',
                  'base/v1/base_pb2_grpc.pyi',
                  'entailment/v1/entailment_pb2.pyi',
                  'entailment/v1/entailment_pb2.pyi',
                  'entailment/v1/entailment_pb2_grpc.pyi',
                  'entailment/v1/entailment_pb2_grpc.pyi',
                  'nlp/v1/nlp_pb2.pyi',
                  'nlp/v1/nlp_pb2.pyi',
                  'nlp/v1/nlp_pb2_grpc.pyi',
                  'nlp/v1/nlp_pb2_grpc.pyi']}

install_requires = \
['grpcio>=1.32,<2.0', 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'arg-services',
    'version': '0.1.5',
    'description': 'GraphQL and gRPC schemas for Microservice-based Argumentation Machines.',
    'long_description': '# Argumentation Microservices\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
