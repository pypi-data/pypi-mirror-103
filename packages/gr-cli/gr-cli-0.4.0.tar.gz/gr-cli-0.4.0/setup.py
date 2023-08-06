# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gr', 'gr.cmd']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0',
 'humanize>=3.4.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['gr = gr.main:app']}

setup_kwargs = {
    'name': 'gr-cli',
    'version': '0.4.0',
    'description': "Gerrit's command line tool",
    'long_description': '# gr\n\nGerrit\'s command line tool\n\n> It\'s like `gh` ([GitHub\'s CLI](https://github.com/cli/cli)) but for Gerrit\n\n![gr screenshot](screenshot.png)\n\n## Installation\n\n```sh\npip3 install gr-cli\n```\n\n## Auth\n\nAuthentication done by `HTTP credentials`: [https://gerrit.cloudlinux.com/settings/#HTTPCredentials](https://gerrit.cloudlinux.com/settings/#HTTPCredentials)\n\nAt first launch, `gr` will ask for username and password that you generated at gerrit and write to `~/.config/gr/conf.py`. That\'s plain python file and you can use it however you want, e.g.:\n\n```python\nimport os\n\npswd = os.popen("pass show cl/gr-cli | head -n 1").read().strip()\nuser = os.popen("pass show cl/gr-cli | grep username").read().strip().split(" ")[-1]\n\nAUTH = (user, pswd)\n```\n\n## Usage\n\n```sh\n> gr ch --help\nUsage: main.py ch [OPTIONS] COMMAND [ARGS]...\n\n  Manage pull requests\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  abandon        Abandon change by ID\n  add-reviewers  Abandon change by ID\n  checkout       Checkout change to new branch\n  comment        Comment change by ID\n  comments       List change comments by ID\n  create         Create change from current branch\n  diff           Show diff by change ID\n  list           List all changes\n  merge          Submit change by ID\n  rebase         Rebase change to target branch by ID\n  review         Review change by ID\n  status         List all CHanges\n  view           View change details\n```\n\n## Example\n\n```sh\ngit checkout -b test-gr\necho Changes > file.txt\ngit add file.txt\ngit commit -m \'New very important patch\'\n\n# push current branch to remote and create PR\ngr ch create\n\ngr ch list\n\ngr ch merge [change-id]\n```\n',
    'author': 'Paul Nameless',
    'author_email': 'reacsdas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paul-nameless/gr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
