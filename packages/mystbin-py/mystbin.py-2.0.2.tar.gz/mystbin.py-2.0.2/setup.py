# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mystbin']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

extras_require = \
{'requests': ['requests>=2.24.0,<3.0.0']}

entry_points = \
{'console_scripts': ['version = mystbin:main']}

setup_kwargs = {
    'name': 'mystbin.py',
    'version': '2.0.2',
    'description': 'A small simple wrapper around the mystb.in API.',
    'long_description': '# MystBin.py!\n\nA small simple wrapper around the [MystB.in](https://mystb.in/) API.\n\n----------\n![Code Linting](https://github.com/AbstractUmbra/mystbin.py/workflows/Code%20Linting/badge.svg?branch=main)\n![Code Analysis](https://github.com/AbstractUmbra/mystbin.py/workflows/Code%20Analysis/badge.svg?branch=main)\n![Build](https://github.com/AbstractUmbra/mystbin.py/workflows/Build/badge.svg)\n### Features\n\n- [x] - `POST`ing to the API, which will return the provided url.\n- [x] - `GET`ting from the API, provided you know the URL or paste ID.\n- [ ] - `DELETE`ing from the API, provided the paste is attached to your account.\n- [ ] - `PATCH`ing to the API, provided the paste is attached to your account.\n- [x] - Ability to pass in a sync or async session / parameter so it is flexible.\n- [x] - Write a real underlying Client for this, it will be required for...\n- [ ] - ... Authorization. Awaiting the API making this public as it is still WIP.\n\n### Installation\nThis project will be on [PyPI](https://pypi.org/project/mystbin.py/) as a stable release, you can always find that there.\n\nInstalling via `pip`:\n```shell\npython -m pip install -U mystbin.py\n# or for optional sync addon...\npython -m pip install -U mystbin.py[requests]\n```\n\nInstalling from source:\n```shell\npython -m pip install git+https://github.com/AbstractUmbra/mystbin-py.git #[requests] for sync addon\n```\n\n### Usage examples\nSince the project is considered multi-sync, it will work in a sync/async environment, see the optional dependency of `requests` below.\n\n```py\n# async example - it will default to async\nimport mystbin\n\nmystbin_client = mystbin.Client()\n#NOTE: The `api_key` kwarg in the Client constructor is optional.\n\npaste = await mystbin_client.post("Hello from MystBin!", syntax="python")\nstr(paste)\n>>> \'https://mystb.in/<your generated ID>.python\'\n\npaste.url\n>>> \'https://mystb.in/<your generated ID>.python\'\n\nget_paste = await mystbin_client.get("https://mystb.in/<your generated ID>")\nstr(get_paste)\n>>> "Hello from MystBin!"\n\npaste.created_at\n>>> datetime.datetime(2020, 10, 6, 10, 53, 57, 556741)\n```\n\n```py\n# sync example - we need to pass a session though\nimport mystbin\nimport requests\n\nsync_session = requests.Session()\nmystbin_client = mystbin.Client(session=sync_session) ## optional api_key kwarg also\n\npaste = mystbin_client.post("Hello from sync Mystb.in!", syntax="text")\nstr(paste)\n>>> \'https://mystb.in/<your generated ID>.text\'\n```\n\nNOTE: the session - aiohttp or requests - will have their default headers changed during init to support the Authorization header with the api key if present, and there is a timeout of 15s for each operation.\n\n### Dependencies\n\n`aiohttp` - required \\\n`requests` - optional',
    'author': 'AbstractUmbra',
    'author_email': 'Umbra@AbstractUmbra.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AbstractUmbra/mystbin-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
