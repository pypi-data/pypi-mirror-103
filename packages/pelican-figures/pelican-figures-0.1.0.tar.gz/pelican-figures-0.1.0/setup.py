# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.figures']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-figures',
    'version': '0.1.0',
    'description': 'Encapsulate standalone images in a figure tag and add a figcaption tag.',
    'long_description': 'Figures: A Plugin for Pelican\n====================================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/figures/build)](https://github.com/f-koehler/pelican-figures/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-figures)](https://pypi.org/project/pelican-figures/)\n![License](https://img.shields.io/pypi/l/pelican-figures?color=blue)\n\nEncapsulate standalone images in a figure tag and add a figcaption tag.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-figures\n\nUsage\n-----\n\n<<Add plugin details here>>\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/f-koehler/pelican-figures/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/pelican-figures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
