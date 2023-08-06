# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['BioPython',
 'dask[array]',
 'fsspec',
 'gcsfs',
 'intervaltree',
 'pandas',
 'petl',
 'petlx',
 'scikit-allel',
 'xarray',
 'zarr']

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '0.5.0a2',
    'description': 'A package for accessing MalariaGEN public data.',
    'long_description': None,
    'author': 'Alistair Miles',
    'author_email': 'alimanfoo@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
