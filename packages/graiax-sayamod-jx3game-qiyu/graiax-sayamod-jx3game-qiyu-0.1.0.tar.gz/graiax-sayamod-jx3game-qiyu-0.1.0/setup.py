# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_jx3game_qiyu', 'graiax_sayamod_jx3game_qiyu.builtins']

package_data = \
{'': ['*'], 'graiax_sayamod_jx3game_qiyu': ['static/*']}

install_requires = \
['graia-application-mirai>=0.17.0,<0.18.0',
 'graia-broadcast>=0.7.0,<0.8.0',
 'graia-saya>=0.0.9,<0.0.10',
 'graia-scheduler>=0.0.4,<0.0.5',
 'pony>=0.7.14,<0.8.0']

setup_kwargs = {
    'name': 'graiax-sayamod-jx3game-qiyu',
    'version': '0.1.0',
    'description': 'A graiax saya mod which is a Jx3 Qiyu Random Collection Game(剑侠情缘网络版三奇遇随机收集游戏) based on group text.',
    'long_description': None,
    'author': 'CowHeadKick',
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
