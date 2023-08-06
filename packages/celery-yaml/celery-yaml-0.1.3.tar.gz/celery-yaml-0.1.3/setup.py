# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['celery_yaml']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'celery>=4']

extras_require = \
{'pyramid': ['pyramid>=1.9', 'plaster-yaml>=0.1.1,<0.2.0']}

setup_kwargs = {
    'name': 'celery-yaml',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
