# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['CloudAtlas']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2021.1,<2022.0', 'requests>=2.25.1,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'cloudatlas',
    'version': '0.0.5',
    'description': 'Python Package for Cloud Atlas Projects',
    'long_description': '# CloudAtlas',
    'author': 'Cloud Atlas',
    'author_email': 'cloud.atlas.br@gmail.com',
    'maintainer': 'Adelmo Filho',
    'maintainer_email': 'adelmo.aguiar.filho@gmail.com',
    'url': 'https://github.com/Cloud-Atlas-BR/CloudAtlas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
