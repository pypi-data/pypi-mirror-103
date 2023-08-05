# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sportbot']

package_data = \
{'': ['*'], 'sportbot': ['tts/*']}

install_requires = \
['asciimatics>=1.13.0,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'gTTS>=2.2.2,<3.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'python-vlc>=3.0.12118,<4.0.0']

entry_points = \
{'console_scripts': ['sportbot = sportbot.main:main']}

setup_kwargs = {
    'name': 'sportbot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adrien Pensart',
    'author_email': 'adrien.pensart@corp.ovh.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
