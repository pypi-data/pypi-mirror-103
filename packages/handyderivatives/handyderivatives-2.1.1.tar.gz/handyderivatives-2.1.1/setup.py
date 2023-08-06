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
    'version': '2.1.1',
    'description': 'Differntiate a list of functions of and auomatically compile a LaTeX document to view the results.',
    'long_description': "# handyderivatives\n\nThis is a command line program to get the derivatives for differentiable functions of a single variable.\n\n## Installation\n`pip install handyderivatives`\n\n[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)\n\n## Running it\nTo get the derivatives for an arbitrary number of functions of a single variable.\n\n`handyderivatives --latex -d 'f(x) = x ^ 2' 'f(x) = sin(x) + 2 * x'` ...\n\nTo get the gradient for an arbitrary number of scalar functions.\n\n`handyderivatives --latex -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'` ...\n\nOr run that at with one command.\n\n`handyderivatives --latex -d 'f(x) = x ^ 2' 'g(x) = sin(x) + 2 * x' -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'`\n\nTo differentiate a list of functions in a file.\n\n`handyderivatives --latex -f functions.txt`\n\n\n```\nusage: handyderivatives [-h] [--input-file FILE] [--latex] [--diff [DIFFERENTIAL [DIFFERENTIAL ...]]] [--gradient [GRADIENT [GRADIENT ...]]]\n\nCommand line differential calculus tool using sympy.\nTry running:\nhandyderivatives -l -g 'f(x,y) = sin(x) * cos(y)'\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --input-file FILE, -f FILE\n                        Input file\n  --latex, -l           Compile a LaTeX document as output\n  --diff [DIFFERENTIAL [DIFFERENTIAL ...]], -d [DIFFERENTIAL [DIFFERENTIAL ...]]\n                        Works for equations written in the form  'f(x) = x ^2'\n  --gradient [GRADIENT [GRADIENT ...]], -g [GRADIENT [GRADIENT ...]]\n                        Works for scalar functions written in form  'f(x,y,z) = x ^2 * sin(y) * cos(z)'\n```\n\n\n\n\n## Opening the output\nNormally you want to immediately see the output, so run something like this.\n\n`handyderivatives -l -d 'sin(x)' && zathura equations.pdf --mode presentation`\n\nThe program used to open the PDF doesn't matter, as long as it's not something like Adobe Reader which takes a couple seconds to open on most machines.\nIf you can enter a PDF and it opens it, then it will work.\nZathura is nice because if you ctl + c in your terminal, or press q in the Zathura window, it will close the PDF.\nThis doesn't happen with them all PDF viewers.\n\n## How the input file should be formatted\nEdit a file that has functions listed one per line.\nThe left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .\nThe right hand side will be the expression.\n\n```\n# This is how the file for the argument -f should be formatted.\n\nc(x) = r * (cos(x) + sqrt(-1) * sin(x))\na(t) = 1/2 * g * t ** 2\nf(x) = sin(x**2) * x^2\nh(w) = E ^ (w^4 - (3 * w)^2 + 9)    # Capital E is interpreted by sympy as the base of the natural log.\ng(x) = exp(3 * pi)                  # So is exp(x), but written as a function taking an argument.\np(j) = csc(j^2)\n```\n\nIf you don't format it like that you will likely run into errors.\nYou  can add comments\n\n## TODO\nRecord screen while the program is executing for an example.\n\nAdd divergence.\n\n## LaTeX PDF output\n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)\n",
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
