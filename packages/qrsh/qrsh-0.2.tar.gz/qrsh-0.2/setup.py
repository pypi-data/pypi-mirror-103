# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrsh']

package_data = \
{'': ['*']}

install_requires = \
['imutils>=0.5.4,<0.6.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pillow',
 'pyzbar>=0.1.8,<0.2.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['qrsh = qrsh.cli:app']}

setup_kwargs = {
    'name': 'qrsh',
    'version': '0.2',
    'description': 'Simple python script for scanning qr codes',
    'long_description': None,
    'author': 'f8ith',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
