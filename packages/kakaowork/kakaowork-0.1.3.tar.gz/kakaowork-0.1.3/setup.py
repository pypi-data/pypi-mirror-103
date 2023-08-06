# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kakaowork']

package_data = \
{'': ['*']}

install_requires = \
['pytz', 'urllib3>=1.26.4,<2.0.0']

extras_require = \
{'cli': ['click>=7.1.2,<8.0.0']}

entry_points = \
{'console_scripts': ['kakaowork = kakaowork.__main__:main']}

setup_kwargs = {
    'name': 'kakaowork',
    'version': '0.1.3',
    'description': 'Kakaowork Python client',
    'long_description': '# kakaowork-py\n\n(Unofficial) Kakaowork Python client\n\n[![CI](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml) [![Documentation Status](https://readthedocs.org/projects/kakaowork-py/badge/?version=latest)](https://kakaowork-py.readthedocs.io/en/latest)\n [![codecov](https://codecov.io/gh/skyoo2003/kakaowork-py/branch/master/graph/badge.svg?token=J6NQHDJEMZ)](https://codecov.io/gh/skyoo2003/kakaowork-py)\n\n__Table of Contents__\n\n- [Prerequisites](#prerequisites)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Prerequisites\n\n- Python >= 3.6.1\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install kakaowork-py\n\n```bash\npip install kakaowork\n```\n\nIf you want to use CLI, install with the extras \'cli\'\n\n```bash\npip install kakaowork[cli]\n```\n\n## Usage\n\n```python\nfrom kakaowork import Kakaowork\n\nclient = Kakaowork(app_key="your_app_key")\nr = client.users.list(limit=10) # get a response of users using limit\nprint(r.users)\nwhile r.cursor: # loop until it does not to exist\n  print(r.users)\n  r = client.users.list(cursor=r.cursor) # get a response of users using cursor\n```\n\nIf you have installed it with the extras \'cli\', you can use the command line below in your shell.\n\n```sh\n$ kakaowork --help\nUsage: kakaowork [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -k, --app-key TEXT\n  --help              Show this message and exit.\n\nCommands:\n  bots\n  conversations\n  departments\n  messages\n  spaces\n  users\n\n$ kakaowork -k <your_app_key> bots info\nID:     1\nName:   Test\nStatus: activated\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## [License](LICENSE)\n\nCopyright (c) 2021 Sung-Kyu Yoo.\n\nThis project is MIT license.\n',
    'author': 'Sung-Kyu Yoo',
    'author_email': 'skyoo2003@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skyoo2003/kakaowork-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
