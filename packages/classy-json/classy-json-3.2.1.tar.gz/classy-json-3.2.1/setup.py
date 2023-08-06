# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classyjson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'classy-json',
    'version': '3.2.1',
    'description': 'Dot-access for Python dictionaries like JS!',
    'long_description': "# Classy-JSON ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/classy-json/badge) ![PYPI Version](https://img.shields.io/pypi/v/classy-json.svg?color=0FAE6E) ![PYPI Downloads](https://img.shields.io/pypi/dw/classy-json?color=0FAE6E) ![Views](https://api.ghprofile.me/view?username=iapetus-11.classy-json&color=0FAE6E&label=views&style=flat)\n*`dict.key` (Dot access) for Python dictionaries*\n\n## How do I use Classy-JSON?\n* Classy-JSON can be used nearly identically to the regular built-in json module! [json module docs](https://docs.python.org/3/library/json.html)\n* The only differences are that you can now access dictionaries via `dict.key` as well as `dict['key']`, and that the `.copy()` method is now a deep copy.\n* What seperates Classy-JSON and its custom data structures from other alternatives? Classy-JSON is both better in its speed and package size, other similiar packages have unecessary code and just aren't as fast as Classy-JSON\n\n## Example Usage\n```py\nimport classyjson as cj\n\n# load data from a json file\nwith open('tests/test_large.json', 'r') as f:\n  data = cj.load(f)\n\n# turn a regular dictionary into a ClassyDict\nmy_dict = {'a': 'b'}\nmy_classy_dict = cj.classify(my_dict)\nprint(my_classy_dict.a)\n\n# or\n\nmy_classy_dict = cj.ClassyDict(my_dict)\nprint(my_classy_dict.a)\n\n# make a new ClassyDict\nnew_classy_dict = cj.ClassyDict()\nnew_classy_dict.a = 'b'\n```\n\n## Setup / Install\n### Using pip:\n```\npython3 -m pip install classy-json\n```\n### Manually:\n* Clone the repository\n```\ngit clone https://github.com/Iapetus-11/Classy-JSON.git\n```\n* cd into the directory\n```\ncd Classy-JSON\n```\n* Run setup.py\n```\npython3 setup.py build install\n```\n\n## Contribution\n* Contributions are welcome! Just submit a pull request!\n",
    'author': 'Milo Weinberg',
    'author_email': 'iapetus011@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Iapetus-11/Classy-JSON',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
