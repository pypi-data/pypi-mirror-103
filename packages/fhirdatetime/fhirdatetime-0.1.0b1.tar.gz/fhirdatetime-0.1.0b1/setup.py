# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fhirdatetime']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fhirdatetime',
    'version': '0.1.0b1',
    'description': 'A datetime-compatible class for FHIR date/datetime values.',
    'long_description': None,
    'author': 'Mike Mabey',
    'author_email': 'mike.mabey@ooda-health.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
