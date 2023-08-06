# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esparto']

package_data = \
{'': ['*'], 'esparto': ['templates/*']}

install_requires = \
['Pillow<9.0.0', 'Pillow>=7.0.0', 'jinja2>=2.10.1,<3.0.0', 'markdown>=3.1,<4.0']

extras_require = \
{'extras': ['beautifulsoup4>=4.9.3,<5.0.0'],
 'test': ['black>=20.8b1,<21.0',
          'flake8>=3.9.0,<4.0.0',
          'mypy>=0.812,<0.813',
          'pytest>=6.2.2,<7.0.0',
          'coverage>=5.5,<6.0',
          'html5lib>=1.1,<2.0']}

setup_kwargs = {
    'name': 'esparto',
    'version': '0.2.0',
    'description': 'Minimal frontend web framework written in Python.',
    'long_description': 'esparto\n=======\n\n[![image](https://img.shields.io/pypi/v/esparto.svg)](https://pypi.python.org/pypi/esparto)\n[![Build Status](https://travis-ci.com/domvwt/esparto.svg?branch=main)](https://travis-ci.com/domvwt/esparto)\n[![codecov](https://codecov.io/gh/domvwt/esparto/branch/main/graph/badge.svg?token=35J8NZCUYC)](https://codecov.io/gh/domvwt/esparto)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=domvwt_esparto&metric=alert_status)](https://sonarcloud.io/dashboard?id=domvwt_esparto)\n\nEsparto is a super minimal frontend web framework written in Python. Its primary use is for generating shareable single page documents\nwith content from popular analytics and data science libraries.\n\nFull documentation and examples at [domvwt.github.io/esparto/](https://domvwt.github.io/esparto/).\n\n### Features\n* Lightweight API\n* No CSS or HTML required\n* Device responsive display\n* Self contained / inline dependencies\n* Jupyter Notebook support\n* MIT License\n\n## Supported Content\n* Markdown text\n* Images\n* Matplotlib figures\n* Pandas DataFrames\n* Bokeh objects\n* Plotly figures\n',
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://domvwt.github.io/esparto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
