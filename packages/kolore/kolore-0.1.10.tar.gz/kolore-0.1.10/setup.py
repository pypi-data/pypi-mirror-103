# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kolore']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['kolore = kolore.cli:parse']}

setup_kwargs = {
    'name': 'kolore',
    'version': '0.1.10',
    'description': 'A small cli utility to convert krita palette files into png images',
    'long_description': '# Kolore\n\nA small cli utility to convert krita palette files into png images.\n\n## Install\n\n`pip install kolore`\n\n## Usage\n\nTo create a palette, simply type\n\n`kolore palette.kpl`\n\nBy default the file will be called `palette.png`, but you can specify another name as well\n\n`kolore palette.kpl --output result.png`\n\nYou can also set the size of the generated image\n\n`kolore palette.kpl --output result.png --width 200 --height 100`\n\nGet general help with\n\n`kolore --help`',
    'author': 'AlvarBer',
    'author_email': 'git@alvarber.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/AlvarBer/kolore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
