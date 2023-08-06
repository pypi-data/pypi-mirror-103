# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ctserial']

package_data = \
{'': ['*']}

install_requires = \
['ctui>=0.7.3,<0.8.0', 'pyserial>=3.5,<4.0', 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['ctserial = ctserial.commands:main']}

setup_kwargs = {
    'name': 'ctserial',
    'version': '0.4.0',
    'description': 'A highly flexible serial interface tool made for penetration testers',
    'long_description': '# Control Things Serial\n\nA highly flexible serial interface tool made for penetration testers.\n\n# Installation:\n\nAs long as you have git and Python 3.6 or later installed, all you should need to do is:\n\n```\npip3 install ctserial\n```\n\n# Usage:\n\nFirst, start the tool from a terminal.  Then connect to your serial device and interact with it.  For example:\n\n```\nctserial> connect /dev/your-serial-device\nctserial> send hex deadc0de        (sends actual hex, so 4 bytes)\nctserial> send Dead Code 国        (sends full utf-8 string without spaces)\nctserial> send "Dead Code 国"      (Use quotes if you need spaces)\nctserial> exit\n```\n\nNOTE: The v0.4.0 temporarily removed non-hex character cleaning from `send hex` hexstring, so you can not currently use spaces in the hex string.  This will be restored in the near future, but I had to push out v0.4.0 a bit fast to replace a broken v0.3.2 which got out of sync with the ctui library it depended on.\n\n# Platform Independence\n\nPython 3.6+ and all dependencies are available for all major operating systems.  It is primarily developed on MacOS and Linux, but should work in Windows as well.\n\n# Development\n\nIf you are interested in modifying `ctserial`:\n\n1. Install Python\'s Poetry package at https://python-poetry.org/.\n2. Clone the `ctserial` github repository.\n3. Open a termainal to the cloned repository.\n4. Run `poetry install` to create a new virtual environment and install an editable instance of `ctserial` with its dependencies.\n\n\n# Author\n\n* Justin Searle <justin@controlthings.io>\n\n',
    'author': 'Justin Searle',
    'author_email': 'justin@controlthings.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.controlthings.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
