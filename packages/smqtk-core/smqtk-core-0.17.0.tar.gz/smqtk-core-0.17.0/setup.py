# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smqtk_core']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=53']

setup_kwargs = {
    'name': 'smqtk-core',
    'version': '0.17.0',
    'description': 'Python toolkit for pluggable algorithms and data structures for multimedia-based machine learning.',
    'long_description': '# SMQTK - Core\n\n## Intent\nProvide a light-weight framework for developing interfaces that have built-in\nimplementation discovery and factory construction from configuration.\n\n## Documentation\nhttps://smqtk-core.readthedocs.io/en/stable/\n\nYou can also build the sphinx documentation locally for the most up-to-date\nreference:\n```bash\n# Install dependencies\npoetry install\n# Navigate to the documentation root.\ncd docs\n# Build the docs.\npoetry run make html\n# Open in your favorite browser!\nfirefox _build/html/index.html\n```\n',
    'author': 'Kitware, Inc.',
    'author_email': 'smqtk-developers@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kitware/SMQTK-Core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
