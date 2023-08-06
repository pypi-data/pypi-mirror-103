# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pigstep', 'pigstep.sounds']

package_data = \
{'': ['*'], 'pigstep': ['templates/*']}

install_requires = \
['beet>=0.22.0', 'pynbs>=0.4.2,<0.5.0']

entry_points = \
{'beet': ['autoload = pigstep.plugin.autoload']}

setup_kwargs = {
    'name': 'pigstep',
    'version': '0.2.1',
    'description': 'A beet plugin for importing songs into Minecraft',
    'long_description': '# pigstep\n\n[![GitHub Actions](https://github.com/vberlier/pigstep/workflows/CI/badge.svg)](https://github.com/vberlier/pigstep/actions)\n[![PyPI](https://img.shields.io/pypi/v/pigstep.svg)](https://pypi.org/project/pigstep/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pigstep.svg)](https://pypi.org/project/pigstep/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A beet plugin for importing songs into Minecraft.\n\n## Introduction\n\nThis [`beet`](https://github.com/mcbeet/beet) plugin lets you include songs created with [Open Note Block Studio](https://opennbs.org/) in your project. It takes care of converting `.nbs` files to data packs.\n\n**Features**\n\n- Keep `.nbs` files alongside the rest of your project\n- Embed note block studio songs into your output data pack\n- Automatically bundle extra notes when needed to support 6 octaves\n- Efficient function tree generation and chord deduplication\n- Flexible, can be used for making custom visualizers\n\n**Why not just export from Note Block Studio directly?**\n\n- It\'s a bit more convenient to set up the plugin once and then have it automatically convert the latest version of the song\n- Less clutter, you can forget about having to navigate around the generated files\n- The plugin bundles the sound files required by your songs, no need to remember to activate the extra notes resource pack or to copy the sounds you need when you start using them\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install pigstep\n```\n\n## Usage\n\nThe plugin generates scoreboard objectives that must be included in the output data pack. If you\'re not using it already, running the `beet.contrib.scoreboard` plugin at the end of the pipeline will create a function that adds all the generated objectives for you.\n\n```json\n{\n  "pipeline": ["pigstep", "beet.contrib.scoreboard"],\n  "meta": {\n    "pigstep": {\n      "load": ["*.nbs"],\n      "source": "ambient",\n      "templates": {\n        "play": "custom_play.mcfunction"\n      }\n    }\n  }\n}\n```\n\nYou can require the plugin programmatically by using the `pigstep` plugin factory.\n\n```python\nfrom beet import Context\nfrom pigstep import pigstep\n\ndef my_plugin(ctx: Context):\n    ctx.require(\n        pigstep(\n            load=["*.nbs"],\n            source="ambient",\n            templates={"play": "custom_play.mcfunction"},\n        )\n    )\n```\n\nAll the configuration is optional. The plugin is a no-op if the `load` option is not specified or empty. The `source` option defaults to `record`. The `templates` option lets you override the templates used by the plugin.\n\nHere are the functions generated for each song:\n\n- `{namespace}:song/{song_name}/play` - Play the song\n- `{namespace}:song/{song_name}/pause` - Pause the song, to resume run the play function again\n- `{namespace}:song/{song_name}/stop` - Stop the song, playing the song again will start from the beginning\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort pigstep tests\n$ poetry run black pigstep tests\n$ poetry run black --check pigstep tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/pigstep/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/pigstep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
