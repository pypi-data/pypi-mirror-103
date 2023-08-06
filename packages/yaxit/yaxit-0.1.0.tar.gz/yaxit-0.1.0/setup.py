# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'yaxit', 'yaxit.integrations']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'bokeh>=2.3.1,<3.0.0',
 'click',
 'h5py>=3.2.1,<4.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tables>=3.6.1,<4.0.0',
 'xarray>=0.17.0,<0.18.0',
 'xpublish>=0.1.0,<0.2.0',
 'xrviz>=0.1.4,<0.2.0']

entry_points = \
{'console_scripts': ['yaxit = yaxit.cli:main']}

setup_kwargs = {
    'name': 'yaxit',
    'version': '0.1.0',
    'description': 'Top-level package for yaxit.',
    'long_description': '=====\nyaxit\n=====\n\n\n.. image:: https://img.shields.io/pypi/v/yaxit.svg\n        :target: https://pypi.python.org/pypi/yaxit\n\n.. image:: https://img.shields.io/travis/jmosbacher/yaxit.svg\n        :target: https://travis-ci.com/jmosbacher/yaxit\n\n.. image:: https://readthedocs.org/projects/yaxit/badge/?version=latest\n        :target: https://yaxit.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nYet Another Xenon Inference Tool\n\n\n* Free software: MIT\n* Documentation: https://yaxit.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/yaxit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
