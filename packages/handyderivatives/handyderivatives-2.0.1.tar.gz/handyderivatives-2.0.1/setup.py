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
    'version': '2.0.1',
    'description': 'Differntiate a list of functions of and auomatically compile a LaTeX document to view the results.',
    'long_description': "# handyderivatives\n\nThis is a command line program to get the derivatives for differentiable functions of a single variable.\n\n## Installation\n`pip install handyderivatives`\n\n[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)\n\n## Running it\nTo simply print back to the terminal.\n\n`handyderivatives -f functions.txt`\n\nTo automatically compile a LaTeX document with pdflatex\n\n`handyderivatives -f functions.txt --latex`\n\n## How the input file should be formatted\nEdit a file that has functions listed one per line.\nThe left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .\nThe right hand side will be the expression.\n\n```\n# This is how the file for the argument -f should be formatted.\n\nc(x) = r * (cos(x) + sqrt(-1) * sin(x))\na(t) = 1/2 * g * t ** 2\nf(x) = sin(x**2) * x^2\nh(w) = E ^ (w^4 - (3 * w)^2 + 9)            # Capital E is interpreted by sympy as the base of the natural log.\ng(x) = exp(3 * pi)                          # So is exp(x), but written as a function taking an argument.\np(j) = csc(j^2)\n```\n\nIf you don't format it like that you will likely run into errors.\nYou  can add comments\n\n## LaTeX PDF output\n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)\n",
    'author': 'fitzy1293',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fitzy1293/handyderivatives',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
