# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphic_coloring_engine', 'graphic_coloring_engine.monkey_patching']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'colormath>=3.0.0,<4.0.0',
 'pydash>=5.0.0,<6.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'graphic-coloring-engine',
    'version': '0.1.2',
    'description': 'graphic coloring engine',
    'long_description': None,
    'author': 'filosfino',
    'author_email': 'github@filosfino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/filosfino/graphic-coloring-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
