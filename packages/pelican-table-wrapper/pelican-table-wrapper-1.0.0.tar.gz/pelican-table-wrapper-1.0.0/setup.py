# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.table_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.0.1,<5.0.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-table-wrapper',
    'version': '1.0.0',
    'description': 'Pelican plugin for wrapping table into classed div',
    'long_description': "[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/table-wrapper/build)](https://github.com/pawo1/table-wrapper/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-table-wrapper)](https://pypi.org/project/pelican-table-wrapper/)\n![License](https://img.shields.io/pypi/l/pelican-table-wrapper?color=blue)\n\nPelican plugin for wrapping table into classed div `.table_wrapper`. It allows \nyou to better style tables. E.g. make them scrollable on small displays.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-table-wrapper\n\nUsage\n-----\n\nTo use this plugin you have to add it to PLUGINS variable in pelicanconf.py:\n```python\nPLUGINS = ['table_wrapper', ...]\n```\n\nIf you don't want add `.table_wrapper` to your CSS, plugin can generate self-styled\nelements. Just specify style that you want in pelicanconf.py:\n```python\nTABLE_WRAPPER = {'style':'overflow: auto;'}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pawo1/table-wrapper/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the MIT license.\n",
    'author': 'Pawo1',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawo1/table-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
