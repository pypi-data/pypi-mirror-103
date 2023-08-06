# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treeshake']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'build', 'cssutils>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'treeshake',
    'version': '0.1.1',
    'description': 'Remove unused css in Python projects with C-powered tree shaking.',
    'long_description': '# treeshake\nA Python / Cython module to include treeshake cascading stylesheets in your projects. Documentation to follow.\n',
    'author': 'j.veldhuis',
    'author_email': 'job@baukefrederik.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jackmanapp/treeshake',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
