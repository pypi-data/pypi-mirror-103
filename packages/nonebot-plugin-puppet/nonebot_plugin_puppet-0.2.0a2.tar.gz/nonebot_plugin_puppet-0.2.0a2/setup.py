# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_puppet']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-puppet',
    'version': '0.2.0a2',
    'description': 'Make Nonebot your puppet',
    'long_description': '# Nonebot Plugin Puppet\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的会话转接插件\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_puppet)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-puppet.svg)\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```\nnb plugin install nonebot_plugin_puppet\n```\n\n- 使用 poetry\n\n```\npoetry add nonebot_plugin_puppet\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_puppet\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\ngit clone https://github.com/Jigsaw111/nonebot_plugin_puppet.git\n```\n\n### 使用\n\n**仅限超级用户使用**\n\n**不建议同时链接多个会话（尤其是大群），如被风控概不负责**\n\n- `puppet link` 链接会话\n- - `-ua user_id ..., --user-a user_id ...` 可选参数，指定源会话的 QQ 号\n- - `-ga group_id ..., --group-b group_id ...` 可选参数，指定源会话的群号\n- - 不设置的话默认为当前会话的 QQ 号/群号\n- - `-u user_id ..., --user-b user_id ...` 可选参数，指定链接会话的 QQ 号\n- - `-g group_id ..., --group-b group_id ...` 可选参数，指定链接会话的群号\n- - 至少需要设置一个\n- `puppet unlink` 取消链接会话\n- - `-ua user_id ..., --user-a user_id ...` 可选参数，指定源会话的 QQ 号\n- - `-ga group_id ..., --group-b group_id ...` 可选参数，指定源会话的群号\n- - 不设置的话默认为当前会话的 QQ 号/群号\n- - `-u user_id ..., --user-b user_id ...` 可选参数，指定链接会话的 QQ 号\n- - `-g group_id ..., --group-b group_id ...` 可选参数，指定链接会话的群号\n- - 不设置的话，默认为当前会话链接的所有会话\n- `puppet list` 查看链接会话列表\n- - `-u user_id, --user user_id` 互斥参数，指定会话的 QQ 号\n- - `-g group_id, --group group_id` 互斥参数，指定会话的群号\n- - 不设置的话默认为当前会话的 QQ 号/群号\n- `puppet send message` 向指定会话发送消息，支持 CQ 码\n- - - `message` 需要发送的消息，支持 CQ 码，如含空格请用 `""` 包裹\n- - `-u user_id ..., --user user_id ...` 可选参数，指定接收会话的 QQ 号\n- - `-g group_id ..., --group group_id ...` 可选参数，指定接收会话的群号\n- - 不设置的话默认为当前会话链接的所有会话\n- - `--a, --all` 可选参数，指定所有群聊\n\n### Q&A\n\n- **这是什么？**  \n  会话转接。\n- **有什么用？**  \n  **没有用**。这个功能一开始是 Dice! 的一部分（具体是不是这功能我不知道，我从没用过），我的移植计划将其从 NoDice 项目中剔除出来（同时剔除的还有一大堆奇奇怪怪的功能），感觉还挺好玩的就写了这么个插件。\n\n<details>\n<summary>展开更多</summary>\n\n### Bug\n\n- [x] 不允许多个超级用户链接到同一会话\n- [x] 如果指定的会话不在会话列表里会产生错误\n\n### To Do\n\n- [ ] 允许单向转接\n- [ ] 转接请求和通知\n\n### Changelog\n\n- 210421 0.2.0-alpha.1\n- - 实现多对多的会话转接\n- - 重构数据结构以便下次更新\n- 210416 0.1.0\n- - 实现单(超级用户)对单(好友,群)的会话转接\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_puppet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
