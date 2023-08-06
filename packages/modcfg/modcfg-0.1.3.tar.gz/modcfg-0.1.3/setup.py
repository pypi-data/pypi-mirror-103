# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modcfg']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'modcfg',
    'version': '0.1.3',
    'description': 'Yes, another config lang',
    'long_description': '# ModCFG\n![YEs](https://raw.githubusercontent.com/ThatXliner/modcfg/master/noo.png)\n\n[![codecov](https://codecov.io/gh/ThatXliner/modcfg/branch/master/graph/badge.svg)](https://codecov.io/gh/ThatXliner/modcfg) [![Documentation Status](https://readthedocs.org/projects/modcfg/badge/?version=latest)](https://modcfg.readthedocs.io/en/latest/?badge=latest) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CI](https://github.com/ThatXliner/modcfg/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/ThatXliner/modcfg/actions/workflows/ci.yml)\n\n> YEs, another configuration language\n\nSeriously, how many configuration languages do we have? From the top of my head, I can only name:\n\n - [JSON](https://www.json.org/)\n - [YAML](https://yaml.org)\n - [INI](https://wikipedia.org/wiki/INI_file)\n - [TOML](https://toml.io/)\n - [XML](https://www.w3.org/XML/)\n\nHmmm... that\'s *it* I think. wE NeEd MOrE cOnfIGURaTion LanGuaGEs!!1!1!!\n\n## But actually though\n\nI originally based this off of the Ruby/DSL for homebrew formulas.\n\nHere are my complaints for the alternatives:\n\n - JSON, while simple, isn\'t too readable and **only has the bear minimum of datatypes.** That may be a feature for some people, though.\n - YAML is [**dangerous**](https://www.arp242.net/yaml-config.html#insecure-by-default). And [**unpredictable**](https://hitchdev.com/strictyaml/why/implicit-typing-removed/).\n - INI and TOML are quite similar and they both are quite nice with a lot of datatypes but, in my opinion, **the format isn\'t as natural to read as YAML**. TOML supports dates and datetime, though.\n - Finally, XML is garbage. It\'s barely human-readable and can decode into a super wonky format. So no.\n\nFinally, I just wanted an excuse to play with Lark.\n\n### Features\n\n - Enums with a built-in resolver\n - Date time and Date support\n - YAML-like syntax\n - Support for comments, **unicode escape sequences**, **string modifications**, and **cleanly managed indented strings**\n\n### Examples\n\nGiven this modcfg document:\n```yaml\nmodule hello_world:\n    hello => world\n    this: "also works"\n    \'single quotes\' = "equals double quotes"\n    how -> {\n            about: {\n                some:\n                    - very\n                    - crazy\n                    - data:\n                        structures = o_0\n            }\n        }\n```\nand this python script:\n```py\nimport modcfg\nmodcfg.loads(DOC)  # `DOC` is the document above\n```\nThe output is\n```py\n[\n    Module(\n        name="hello_world",\n        contents=[\n            {\n                "hello": "world",\n                "this": "also works",\n                "single quotes": "equals double quotes",\n                "how": {\n                    "about": {\n                        "some": ["very", "crazy", {"data": {"structures": "o_0"}}]\n                    }\n                },\n            }\n        ],\n    )\n]\n```\nCrazy, right? It gets better with enums and date(time)s... You might as well read the whole [documentation][documentation].\n\n## Installation\n```bash\n$ pip install modcfg\n```\n### Develop-install\n\nThe classic method:\n\n```bash\n$ git clone https://github.com/ThatXliner/modcfg.git\n$ cd modcfg\n$ python3 -m venv .venv\n$ source .venv/bin/activate\n$ pip install -e .\n```\n\nThe best method (requires [Poetry](https://python-poetry.org/)):\n\n```bash\n$ git clone https://github.com/ThatXliner/modcfg.git\n$ cd modcfg\n$ poetry install\n```\n\n## FAQ\n\n### Why did you make this\n\n![why](https://raw.githubusercontent.com/ThatXliner/modcfg/master/why.png)\n\n[Lark](https://github.com/lark-parser/lark) is epic.\n\n### Why the name?\n\n**Mod**ular **C**on**f**i**g**uration language.\n\n[documentation]: https://modcfg.readthedocs.io/en/latest/index.html\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/modcfg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
