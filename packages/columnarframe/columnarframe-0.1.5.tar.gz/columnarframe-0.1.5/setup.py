# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['columnarframe']

package_data = \
{'': ['*']}

install_requires = \
['pyarrow>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'columnarframe',
    'version': '0.1.5',
    'description': '',
    'long_description': '# ColumnarFrame\n\nカラムベースでデータを扱うためのライブラリです。\nある程度Pandasのように操作できるような形を目指しています。\n\nThis is a library for handling column-based data.\nIt is intended to be operated like Pandas to some extent.\n',
    'author': 'tamuto',
    'author_email': 'tamuto@infodb.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tamuto/columnarframe',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
