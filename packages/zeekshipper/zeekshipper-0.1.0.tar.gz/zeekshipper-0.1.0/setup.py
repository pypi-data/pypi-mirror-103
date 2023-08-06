# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeekshipper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'fastparquet>=0.5.0,<0.6.0',
 'minio>=7.0.3,<8.0.0',
 'pathlib>=1.0.1,<2.0.0',
 's3fs>=2021.4.0,<2022.0.0',
 'zat>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['zeekshipper = zeekshipper.zeeker:log_minio_trino']}

setup_kwargs = {
    'name': 'zeekshipper',
    'version': '0.1.0',
    'description': 'using it:.log to parquet,and push it to minio,final back to you a .txt file with cmd-line for trino to build table.',
    'long_description': None,
    'author': 'Mutu',
    'author_email': 'mutou_nan@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
