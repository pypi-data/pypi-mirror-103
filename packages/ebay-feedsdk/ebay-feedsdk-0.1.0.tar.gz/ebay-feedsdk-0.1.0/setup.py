# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ebay_feedsdk',
 'ebay_feedsdk.config',
 'ebay_feedsdk.constants',
 'ebay_feedsdk.enums',
 'ebay_feedsdk.errors',
 'ebay_feedsdk.examples',
 'ebay_feedsdk.feed',
 'ebay_feedsdk.filter',
 'ebay_feedsdk.tests',
 'ebay_feedsdk.utils']

package_data = \
{'': ['*'],
 'ebay_feedsdk': ['sample-config/*'],
 'ebay_feedsdk.tests': ['test-data/*']}

setup_kwargs = {
    'name': 'ebay-feedsdk',
    'version': '0.1.0',
    'description': 'Port of https://github.com/eBay/FeedSDK-Python to python3',
    'long_description': None,
    'author': 'Lars Erler',
    'author_email': 'lars@xaospage.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
