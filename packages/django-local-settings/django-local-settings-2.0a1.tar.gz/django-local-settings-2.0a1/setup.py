# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['local_settings']

package_data = \
{'': ['*']}

install_requires = \
['Django']

entry_points = \
{'console_scripts': ['make-local-settings = '
                     'local_settings:make_local_settings']}

setup_kwargs = {
    'name': 'django-local-settings',
    'version': '2.0a1',
    'description': 'Define Django settings using TOML',
    'long_description': None,
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/django-local-settings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
