# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ulogcorn']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'ulogcorn',
    'version': '0.4.0',
    'description': 'Unify logging for a gunicorn and uvicorn application with loguru',
    'long_description': None,
    'author': '欧德天.尼维森莫.纳墨迪奥',
    'author_email': 'icocoabeans@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
