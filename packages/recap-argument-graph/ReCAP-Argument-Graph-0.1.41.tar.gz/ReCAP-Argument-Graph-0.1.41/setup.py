# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recap_argument_graph']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.13.2,<0.14.0',
 'lxml>=4.4.2,<5.0.0',
 'networkx>=2.4,<3.0',
 'pendulum>=2.0,<3.0']

extras_require = \
{'docs': ['sphinx>=3.5,<4.0',
          'sphinx-autodoc-typehints>=1.11,<2.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'myst-parser>=0.13.7,<0.14.0']}

setup_kwargs = {
    'name': 'recap-argument-graph',
    'version': '0.1.41',
    'description': 'A library for loading argument graphs in various formats (e.g., AIF).',
    'long_description': '# ReCAP Argument Graph\n\nThe documentation is hosted on `Read the Docs`:\n\n[![Documentation Status](https://readthedocs.org/projects/recap-argument-graph/badge/?version=latest)](https://recap-argument-graph.readthedocs.io/en/latest/?badge=latest)\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
