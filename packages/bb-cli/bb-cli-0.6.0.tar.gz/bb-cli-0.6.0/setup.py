# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bb', 'bb.cmd']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0',
 'humanize>=3.4.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['bb = bb.main:app']}

setup_kwargs = {
    'name': 'bb-cli',
    'version': '0.6.0',
    'description': "Bitbucket's command line tool",
    'long_description': '# bb\n\nBitbucket\'s command line tool\n\n> It\'s like `gh` ([GitHub\'s CLI](https://github.com/cli/cli)) but for BitBucket\n\nThis tools is very basic but it does all what I need at the moment (though I am happy to accept PRs)\n\n![bb screenshot](screenshot.png)\n\n## Installation\n\n```sh\npip3 install bb-cli\n```\n\n## Auth\n\nAt the moment the only way it works is by `App passwords` auth: [https://bitbucket.org/account/settings/app-passwords/](https://bitbucket.org/account/settings/app-passwords/)\n\n> For this you need to have 2FA enabled\n\nAt first launch, `bb` will ask for user and password that you generated at bitbucket and write to `~/.config/bb/conf.py`. That\'s plain python file and you can use it to store information securely:\n\n```python\nimport os\n\npswd = os.popen("pass show ep/bb-cli | head -n 1").read().strip()\nuser = os.popen("pass show ep/bb-cli | grep username").read().strip().split(" ")[-1]\n\nAUTH = (user, pswd)\n```\n\n## Usage\n\n```sh\n> bb pr --help\nUsage: bb pr [OPTIONS] COMMAND [ARGS]...\n\n  Manage pull requests\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  approve          Approve PR by ID\n  checkout         Checkout PR by ID\n  comments         View comments for PR by ID\n  commits          View commits of PR by ID\n  create           Create new PR\n  decline          Decline PR by ID\n  diff             Show diff by PR ID\n  list             List all PRs\n  merge            Merge PR by ID\n  request-changes  Request changes for PR by ID\n  status           Shows more detailed information about PRs (Build,...\n```\n\n## Example\n\n```sh\ngit checkout -b test-bb\necho Changes > file.txt\ngit add file.txt\ngit commit -m \'New very important patch\'\n\n# push current branch to remote and create PR\nbb pr create\n\nbb pr status\n\nbb pr merge 1\n```\n',
    'author': 'Paul Nameless',
    'author_email': 'reacsdas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paul-nameless/bb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
