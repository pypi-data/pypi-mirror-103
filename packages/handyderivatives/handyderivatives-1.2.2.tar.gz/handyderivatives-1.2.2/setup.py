# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handyderivatives']

package_data = \
{'': ['*']}

install_requires = \
['sympy>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['handyderivatives = handyderivatives:main']}

setup_kwargs = {
    'name': 'handyderivatives',
    'version': '1.2.2',
    'description': 'A simple little program to batch process some basic calc stuff.',
    'long_description': '# handyderivatives\n\nInstall with pip for the easiest use.\n\n`pip install handyderivatives`\n\n[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)\n\n## Running it\n`handyderivatives functions.txt`\n\n## How to use it\nIt gets the derivatives for differentiable functions of a single variable.\n\nEdit a file that looks like this. \n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/file.png)\n\nTo get output that looks like this. LaTex output is included.\n\n**If you install with pip just run handyderivatives, this image was from before it was published.**\n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/output.png)\n',
    'author': 'fitzy1293',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fitzy1293/handyderivatives',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
