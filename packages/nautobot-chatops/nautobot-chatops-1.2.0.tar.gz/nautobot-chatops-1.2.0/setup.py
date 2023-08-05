# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_chatops',
 'nautobot_chatops.api',
 'nautobot_chatops.api.views',
 'nautobot_chatops.dispatchers',
 'nautobot_chatops.management.commands',
 'nautobot_chatops.migrations',
 'nautobot_chatops.tests',
 'nautobot_chatops.tests.workers',
 'nautobot_chatops.workers']

package_data = \
{'': ['*'], 'nautobot_chatops': ['static/nautobot/*', 'templates/nautobot/*']}

install_requires = \
['nautobot',
 'nautobot-capacity-metrics',
 'pyjwt[crypto]>=1.7.1,<2.0.0',
 'slack-sdk>=3.4.2,<4.0.0',
 'texttable>=1.6.2,<2.0.0',
 'webexteamssdk>=1.3,<2.0']

entry_points = \
{'nautobot.workers': ['clear = nautobot_chatops.workers.clear:clear',
                      'nautobot = nautobot_chatops.workers.nautobot:nautobot']}

setup_kwargs = {
    'name': 'nautobot-chatops',
    'version': '1.2.0',
    'description': 'A plugin providing chatbot capabilities for Nautobot',
    'long_description': '# nautobot-chatops\n\nA multi-platform ChatOps bot plugin for [Nautobot](https://github.com/nautobot/nautobot).\n\n- Support for multiple chat platforms (currently Slack, Microsoft Teams, and WebEx Teams)\n- Write a command once and run it on every supported platform, including rich content formatting\n- Extensible - other Nautobot plugins can provide additional commands which will be dynamically discovered.\n- Automatic generation of basic help menus (accessed via `help`, `/command help`, or `/command sub-command help`)\n- Metrics of command usage via the `nautobot_capacity_metrics` plugin.\n\n## Documentation\n\n- [Installation Guide](docs/chat_setup.md)\n- [Design](docs/design.md)\n- [Contributing](docs/contributing.md)\n- [FAQ](docs/FAQ.md)\n\n## Contributing\n\nThank you for your interest in helping to improve Nautobot!\nRefer to the [contributing guidelines](docs/contributing.md) for details.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](docs/FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #nautobot).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-chatops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
