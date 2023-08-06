# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scml_vis', 'scml_vis.vendor', 'scml_vis.vendor.quick']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'click-config-file>=0.6.0,<0.7.0',
 'click>=7.1.2,<8.0.0',
 'csvs-to-sqlite>=1.2,<2.0',
 'datasette-vega>=0.6.2,<0.7.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'streamlit>=0.80.0,<0.81.0',
 'watchdog>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['scml-vis = scml_vis.cli:main',
                     'scmlv = scml_vis.cli:main',
                     'scmlvis = scml_vis.cli:main']}

setup_kwargs = {
    'name': 'scml-vis',
    'version': '0.2.0',
    'description': 'A simple visualiser for SCML worlds and tournaments',
    'long_description': '# scml-vis\n\n[![ci](https://github.com/yasserfarouk/scml-vis/actions/workflows/main.yml/badge.svg)](https://github.com/yasserfarouk/scml-vis/actions/workflows/main.yml)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://scml-vis.github.io/scml-vis/)\n[![pypi version](https://img.shields.io/pypi/v/scml-vis.svg)](https://pypi.org/project/scml-vis/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/scml-vis/community)\n\nA simple visualiser for SCML worlds and tournaments\n\n## Screenshots\n![Screen Shot 1](docs/shot1.png)\n![Screen Shot 2](docs/shot2.png)\n\n## Main Features\n\n- Displays any world/tournament run using the [SCML package](https://www.github.com/yasserfarouk/scml)\n- Allows filtering using worlds, agent types, and agent instances\n- Shows world statistics, agent type and instance statistics and contract \n  statistics as functions of simulation step/time\n\n## TODO List (Good Ideas for PRs)\n\n- Show negotiation logs (i.e. negotiation results)\n- Display all contracts (i.e. in a table) based on selection criteria\n- Zoom on negotiation details (i.e. exchanged offers)\n- Add dynamic figures using plotly/altair\n- Add networkx like graphs of contracts / negotiations / offers\n- Add new figure types that do not have time/step in the x-axis\n- Allow starting the app without specifying a folder. In this case, it should \n  have a dropdown list showing the latest tournament/world runs (requires \n  changes to [scml](https://www.github.com/yasserfarouk/scml))\n\n## Requirements\n\nscml-vis requires Python 3.8 or above.\n\n## Installation\n\nWith `pip`:\n```bash\npython3 -m pip install scml-vis\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3 -m pip install --user pipx\n\npipx install scml-vis\n```\n',
    'author': 'Yasser Mohammad',
    'author_email': 'yasserfarouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scml-vis/scml-vis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
