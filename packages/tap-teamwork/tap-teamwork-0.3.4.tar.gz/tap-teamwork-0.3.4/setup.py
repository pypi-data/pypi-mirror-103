# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_teamwork', 'tap_teamwork.tests']

package_data = \
{'': ['*'], 'tap_teamwork': ['schemas/*']}

install_requires = \
['singer-sdk>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['tap-teamwork = tap_teamwork.tap:cli']}

setup_kwargs = {
    'name': 'tap-teamwork',
    'version': '0.3.4',
    'description': 'Singer.io tap for Teamwork.com',
    'long_description': "# tap-teamwork\n\n**Author**: Stephen Bailey (sbailey@immuta.com)\n\nThis is a [Singer](http://singer.io) tap for [Teamwork.com](https://teamwork.com) that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).\n\nIt can generate a catalog of available data in teamwork and extract the following resources:\n\n- Projects\n- Project updates\n- Project milestones\n- Project risks\n- Latest project activity\n- People\n- Tags\n\n### Quick Start\n\n1. Install\n\n```bash\ngit clone git@github.com:immuta/tap-teamwork.git\ncd tap-teamwork\npip install .\n```\n\n2. Get an API key from Teamwork's website.\n\n3. Create the config file.\n\nThere is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your token\n\n4. Run the application to generate a catalog.\n\n```bash\ntap-teamwork -c config.json --discover > catalog.json\n```\n\n5. Select the tables you'd like to replicate\n\nStep 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields. You'll need to open the file and select the ones you'd like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.\n\n6. Run it!\n\n```bash\ntap-teamwork -c config.json --catalog catalog.json\n```\n\n### Acknowledgements\n\nWould like to acknowledge the folks at Fishtown Analytics whose [`tap-framework`](https://github.com/fishtown-analytics/tap-framework) and [`tap-lever`](https://github.com/fishtown-analytics/tap-lever) packages formed the foundation for this package.\n\nCopyright &copy; 2020 Immuta\n",
    'author': 'Stephen Bailey',
    'author_email': 'stkbailey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/immuta/tap-teamwork',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
