# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethicalai']

package_data = \
{'': ['*']}

install_requires = \
['aif360[all]>=0.4.0,<0.5.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'ethicalai',
    'version': '0.0.0',
    'description': 'Open source Ethical AI toolkit',
    'long_description': None,
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alves.da.costa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
