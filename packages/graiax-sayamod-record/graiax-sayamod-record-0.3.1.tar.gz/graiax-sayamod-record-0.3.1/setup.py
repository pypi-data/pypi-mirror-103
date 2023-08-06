# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_record']

package_data = \
{'': ['*'],
 'graiax_sayamod_record': ['.git/*',
                           '.git/hooks/*',
                           '.git/info/*',
                           '.git/logs/*',
                           '.git/logs/refs/heads/*',
                           '.git/objects/0c/*',
                           '.git/objects/21/*',
                           '.git/objects/22/*',
                           '.git/objects/3b/*',
                           '.git/objects/3d/*',
                           '.git/objects/8c/*',
                           '.git/objects/93/*',
                           '.git/objects/9c/*',
                           '.git/objects/ae/*',
                           '.git/objects/b4/*',
                           '.git/objects/c1/*',
                           '.git/objects/db/*',
                           '.git/objects/f4/*',
                           '.git/refs/heads/*',
                           '.vscode/*']}

install_requires = \
['graia-application-mirai>=0.17.0,<0.18.0',
 'graia-broadcast>=0.7.0,<0.8.0',
 'graia-saya>=0.0.9,<0.0.10',
 'pony>=0.7.14,<0.8.0']

setup_kwargs = {
    'name': 'graiax-sayamod-record',
    'version': '0.3.1',
    'description': 'A graia saya mod to record message in databases.',
    'long_description': None,
    'author': 'hans',
    'author_email': 'dxzenghan@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
